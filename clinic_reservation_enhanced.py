import simpy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
from scipy import stats

class EnhancedClinicReservationSystem:
    def __init__(self, env, doctor_config, mean_consult_times, patient_arrival_rates, 
                 patient_type_probabilities, scheduling_strategy="fifo", historical_data=None):
        self.env = env
        
        # Dokter berdasarkan spesialisasi
        self.doctors = {}
        for specialty, count in doctor_config.items():
            self.doctors[specialty] = simpy.PriorityResource(env, capacity=count)
        
        self.mean_consult_times = mean_consult_times  # Dict: jenis_pasien -> waktu konsultasi
        self.patient_arrival_rates = patient_arrival_rates  # Dict: jenis_pasien -> arrival rate
        self.patient_type_probabilities = patient_type_probabilities  # Distribusi tipe pasien
        self.scheduling_strategy = scheduling_strategy  # Strategi penjadwalan
        self.historical_data = historical_data  # Data historis untuk validasi
        
        # Statistik umum
        self.waiting_times = defaultdict(list)  # Berdasarkan tipe pasien
        self.service_times = defaultdict(list)  # Berdasarkan tipe pasien
        self.queue_lengths = defaultdict(list)  # Berdasarkan spesialisasi
        self.doctor_busy_time = defaultdict(float)  # Berdasarkan spesialisasi
        self.total_patients = defaultdict(int)  # Jumlah pasien berdasarkan tipe
        self.unserved_patients = defaultdict(int)  # Pasien yang tidak dilayani
        
        # Untuk monitoring
        self.last_queue_length_update = 0
        self.last_queue_lengths = {specialty: 0 for specialty in doctor_config.keys()}
        
        # Monitor antrian setiap menit
        env.process(self.monitor_queue())
    
    def monitor_queue(self):
        while True:
            current_time = self.env.now
            time_diff = current_time - self.last_queue_length_update
            
            # Tambahkan panjang antrian sebelumnya berdasarkan waktu berlalu
            if time_diff > 0:
                for specialty, queue_length in self.last_queue_lengths.items():
                    self.queue_lengths[specialty].extend([queue_length] * int(time_diff))
            
            # Update nilai terakhir
            for specialty, doctor_resource in self.doctors.items():
                self.last_queue_lengths[specialty] = len(doctor_resource.queue)
            
            self.last_queue_length_update = current_time
            yield self.env.timeout(1)
    
    def get_doctor_priority(self, patient_type, patient_urgency):
        """Menentukan prioritas untuk antrian dokter berdasarkan jenis pasien dan urgensi"""
        # Prioritas lebih rendah = lebih tinggi (dalam simpy PriorityResource)
        if self.scheduling_strategy == "priority":
            # Berdasarkan urgensi (1=paling urgent, 5=paling tidak urgent)
            return patient_urgency
        elif self.scheduling_strategy == "type_based":
            # Berdasarkan tipe pasien (misalnya, 'emergency' = 1, 'regular' = 3)
            priorities = {"emergency": 1, "urgent": 2, "regular": 3, "followup": 4, "checkup": 5}
            return priorities.get(patient_type, 3)  # Default ke 'regular' jika tipe tidak dikenali
        else:
            # FIFO - semua pasien prioritas sama
            return 3
    
    def get_appropriate_specialty(self, patient_type):
        """Menentukan spesialisasi dokter yang sesuai untuk jenis pasien"""
        # Mapping sederhana, bisa dibuat lebih kompleks
        specialty_mapping = {
            "emergency": "general",
            "urgent": "general",
            "regular": "general",
            "checkup": "preventive",
            "followup": "followup",
            "cardiology": "specialist",
            "dermatology": "specialist",
            "pediatrics": "specialist"
        }
        return specialty_mapping.get(patient_type, "general")
    
    def patient_arrival(self, patient_id, patient_type, urgency=3):
        """Proses kedatangan pasien dengan tipe dan tingkat urgensi"""
        arrival_time = self.env.now
        self.total_patients[patient_type] += 1
        
        # Tentukan spesialisasi dokter yang dibutuhkan
        required_specialty = self.get_appropriate_specialty(patient_type)
        
        # Hitung prioritas berdasarkan strategi penjadwalan
        priority = self.get_doctor_priority(patient_type, urgency)
        
        try:
            # Request dokter dengan prioritas
            with self.doctors[required_specialty].request(priority=priority) as request:
                # Tunggu sampai dokter tersedia atau timeout setelah 120 menit
                results = yield request | self.env.timeout(120)
                
                if request in results:
                    # Dokter tersedia, catat waktu tunggu
                    wait_time = self.env.now - arrival_time
                    self.waiting_times[patient_type].append(wait_time)
                    
                    # Lakukan konsultasi dengan waktu berdasarkan tipe pasien
                    mean_time = self.mean_consult_times[patient_type]
                    # Variasi waktu konsultasi (distribusi gamma lebih realistis)
                    shape, scale = 4, mean_time/4  # Shape=4 untuk cv=0.5
                    consult_time = np.random.gamma(shape, scale)
                    
                    self.service_times[patient_type].append(consult_time)
                    self.doctor_busy_time[required_specialty] += consult_time
                    
                    # Simulasikan waktu konsultasi
                    yield self.env.timeout(consult_time)
                    
                    # Peluang untuk tindak lanjut
                    if random.random() < 0.2 and patient_type != "followup":
                        # Jadwalkan kunjungan tindak lanjut dalam 30-60 hari
                        followup_time = random.randint(30, 60) * 480  # Dalam menit
                        yield self.env.timeout(followup_time)
                        self.env.process(self.patient_arrival(patient_id + 10000, "followup", urgency=4))
                else:
                    # Timeout, pasien tidak dilayani
                    self.unserved_patients[patient_type] += 1
        except:
            # Penanganan kesalahan
            self.unserved_patients[patient_type] += 1
            
    def validate_with_historical_data(self):
        """Validasi model dengan data historis"""
        if self.historical_data is None:
            return {"valid": False, "reason": "No historical data provided"}
        
        # Hitung metrik untuk perbandingan
        model_metrics = {
            "avg_wait_time": {
                pt: np.mean(times) if times else 0 
                for pt, times in self.waiting_times.items()
            },
            "avg_service_time": {
                pt: np.mean(times) if times else 0 
                for pt, times in self.service_times.items()
            },
            "doctor_utilization": {}
        }
        
        # Hitung utilisasi dokter dengan pengecekan division by zero
        for spec in self.doctors:
            total_time = self.env.now * len(self.doctors[spec].users)
            if total_time > 0:
                utilization = (self.doctor_busy_time[spec] / total_time) * 100
            else:
                utilization = 0
            model_metrics["doctor_utilization"][spec] = utilization
        
        # Bandingkan dengan data historis
        validation_results = {}
        for metric, model_values in model_metrics.items():
            if metric in self.historical_data:
                historical_values = self.historical_data[metric]
                
                # Hitung persentase error
                errors = {}
                for key in model_values:
                    if key in historical_values and historical_values[key] > 0:
                        error = abs(model_values[key] - historical_values[key]) / historical_values[key] * 100
                        errors[key] = error
                
                validation_results[metric] = {
                    "mean_error_percent": np.mean(list(errors.values())) if errors else 0,
                    "errors": errors
                }
        
        # Tentukan apakah model valid (error < 15%)
        is_valid = all(res["mean_error_percent"] < 15 for res in validation_results.values())
        
        return {
            "valid": is_valid,
            "results": validation_results
        }


def generate_patients(env, system):
    """Fungsi untuk generate pasien berdasarkan tipe"""
    patient_id = 0
    
    while True:
        # Tentukan tipe pasien yang akan datang
        patient_type = random.choices(
            list(system.patient_type_probabilities.keys()),
            weights=list(system.patient_type_probabilities.values()),
            k=1
        )[0]
        
        # Waktu antar kedatangan berdasarkan tipe pasien
        interarrival_time = random.expovariate(system.patient_arrival_rates[patient_type])
        yield env.timeout(interarrival_time)
        
        # Tentukan urgensi pasien (1-5, 1 paling urgent)
        if patient_type == "emergency":
            urgency = random.choices([1, 2], weights=[0.7, 0.3], k=1)[0]
        elif patient_type == "urgent":
            urgency = random.choices([2, 3], weights=[0.6, 0.4], k=1)[0]
        elif patient_type == "regular":
            urgency = random.choices([3, 4], weights=[0.7, 0.3], k=1)[0]
        else:
            urgency = random.choices([3, 4, 5], weights=[0.2, 0.5, 0.3], k=1)[0]
        
        # Pasien baru tiba
        patient_id += 1
        env.process(system.patient_arrival(patient_id, patient_type, urgency))


def run_enhanced_simulation(doctor_config, mean_consult_times, patient_arrival_rates, 
                           patient_type_probabilities, scheduling_strategy="fifo", 
                           historical_data=None, sim_time=480):
    """Jalankan simulasi klinik yang ditingkatkan"""
    env = simpy.Environment()
    
    # Buat sistem reservasi klinik yang ditingkatkan
    system = EnhancedClinicReservationSystem(
        env, doctor_config, mean_consult_times, patient_arrival_rates,
        patient_type_probabilities, scheduling_strategy, historical_data
    )
    
    # Mulai proses kedatangan pasien
    env.process(generate_patients(env, system))
    
    # Jalankan simulasi
    env.run(until=sim_time)
    
    # Hitung statistik
    results = {"scheduling_strategy": scheduling_strategy}
    
    # Waktu tunggu berdasarkan tipe pasien
    avg_wait_times = {
        pt: np.mean(times) if times else 0 
        for pt, times in system.waiting_times.items()
    }
    results["avg_wait_time_by_type"] = avg_wait_times
    results["overall_avg_wait_time"] = np.mean([t for times in system.waiting_times.values() for t in times]) if any(system.waiting_times.values()) else 0
    
    # Waktu layanan berdasarkan tipe pasien
    avg_service_times = {
        pt: np.mean(times) if times else 0 
        for pt, times in system.service_times.items()
    }
    results["avg_service_time_by_type"] = avg_service_times
    
    # Panjang antrian berdasarkan spesialisasi
    avg_queue_lengths = {
        spec: np.mean(lengths) if lengths else 0 
        for spec, lengths in system.queue_lengths.items()
    }
    results["avg_queue_length_by_specialty"] = avg_queue_lengths
    
    # Utilisasi dokter berdasarkan spesialisasi
    doctor_utilizations = {
        spec: system.doctor_busy_time[spec] / (sim_time * doctor_config[spec]) * 100 
        for spec in doctor_config
    }
    results["doctor_utilization_by_specialty"] = doctor_utilizations
    results["overall_doctor_utilization"] = np.mean(list(doctor_utilizations.values()))
    
    # Jumlah pasien
    results["patient_counts"] = dict(system.total_patients)
    results["total_patients"] = sum(system.total_patients.values())
    
    # Pasien yang tidak dilayani
    results["unserved_patients"] = dict(system.unserved_patients)
    results["total_unserved"] = sum(system.unserved_patients.values())
    results["service_rate"] = (results["total_patients"] - results["total_unserved"]) / results["total_patients"] * 100 if results["total_patients"] > 0 else 0
    
    # Validasi model
    if historical_data:
        results["validation"] = system.validate_with_historical_data()
    
    return results, system


def sensitivity_analysis(param_ranges, fixed_params, sim_time=480, replications=5):
    """Analisis sensitivitas dengan variasi parameter"""
    results = []
    
    for param_name, param_values in param_ranges.items():
        for param_value in param_values:
            # Buat salinan parameter tetap dan ubah parameter yang dianalisis
            params = fixed_params.copy()
            
            # Update parameter yang bervariasi
            if param_name == "doctor_config":
                params["doctor_config"] = param_value
            elif param_name == "mean_consult_times":
                # Perbarui mean_consult_times untuk tipe pasien tertentu atau semua
                if isinstance(param_value, dict):
                    for pt, val in param_value.items():
                        params["mean_consult_times"][pt] = val
                else:
                    # Jika nilai tunggal, apply ke semua tipe pasien
                    for pt in params["mean_consult_times"]:
                        params["mean_consult_times"][pt] = param_value
            elif param_name == "patient_arrival_rates":
                if isinstance(param_value, dict):
                    for pt, val in param_value.items():
                        params["patient_arrival_rates"][pt] = val
                else:
                    # Jika nilai tunggal, apply scale factor ke semua tipe pasien
                    for pt in params["patient_arrival_rates"]:
                        params["patient_arrival_rates"][pt] *= param_value
            elif param_name == "scheduling_strategy":
                params["scheduling_strategy"] = param_value
            
            # Jalankan replications untuk parameter ini
            replication_results = []
            for rep in range(replications):
                result, _ = run_enhanced_simulation(
                    doctor_config=params["doctor_config"],
                    mean_consult_times=params["mean_consult_times"],
                    patient_arrival_rates=params["patient_arrival_rates"],
                    patient_type_probabilities=params["patient_type_probabilities"],
                    scheduling_strategy=params["scheduling_strategy"],
                    historical_data=params.get("historical_data"),
                    sim_time=sim_time
                )
                replication_results.append(result)
            
            # Hitung rata-rata dari replications
            avg_result = {
                "parameter": param_name,
                "value": param_value if not isinstance(param_value, dict) else str(param_value),
                "overall_avg_wait_time": np.mean([r["overall_avg_wait_time"] for r in replication_results]),
                "overall_doctor_utilization": np.mean([r["overall_doctor_utilization"] for r in replication_results]),
                "service_rate": np.mean([r["service_rate"] for r in replication_results]),
            }
            
            results.append(avg_result)
            
            print(f"Parameter: {param_name}, Value: {avg_result['value']}")
            print(f"  Average Wait Time: {avg_result['overall_avg_wait_time']:.2f} minutes")
            print(f"  Doctor Utilization: {avg_result['overall_doctor_utilization']:.2f}%")
            print(f"  Service Rate: {avg_result['service_rate']:.2f}%")
            print("-" * 50)
    
    return pd.DataFrame(results)


def optimize_parameters(param_space, objective_function, constraints, sim_time=480, replications=3):
    """Optimasi parameter sistem untuk mencapai tujuan tertentu dengan batasan"""
    best_solution = None
    best_score = float('-inf') if objective_function["direction"] == "maximize" else float('inf')
    
    results = []
    
    # Coba setiap kombinasi parameter
    total_combinations = 1
    for param_values in param_space.values():
        total_combinations *= len(param_values)
    
    print(f"Total kombinasi parameter: {total_combinations}")
    
    combination_count = 0
    for doctor_config in param_space["doctor_config"]:
        for strategy in param_space["scheduling_strategy"]:
            # Parameter lainnya bisa ditambahkan sesuai kebutuhan
            
            combination_count += 1
            print(f"Evaluasi kombinasi {combination_count}/{total_combinations}")
            
            # Siapkan parameter untuk simulasi
            params = {
                "doctor_config": doctor_config,
                "mean_consult_times": param_space["mean_consult_times"][0],  # Gunakan nilai pertama
                "patient_arrival_rates": param_space["patient_arrival_rates"][0],  # Gunakan nilai pertama
                "patient_type_probabilities": param_space["patient_type_probabilities"][0],  # Gunakan nilai pertama
                "scheduling_strategy": strategy
            }
            
            # Jalankan replications
            replication_results = []
            for rep in range(replications):
                result, _ = run_enhanced_simulation(**params, sim_time=sim_time)
                replication_results.append(result)
            
            # Hitung rata-rata metrik
            avg_metrics = {
                "overall_avg_wait_time": np.mean([r["overall_avg_wait_time"] for r in replication_results]),
                "overall_doctor_utilization": np.mean([r["overall_doctor_utilization"] for r in replication_results]),
                "service_rate": np.mean([r["service_rate"] for r in replication_results]),
            }
            
            # Evaluasi constraint
            constraints_satisfied = True
            for constraint in constraints:
                metric = constraint["metric"]
                operator = constraint["operator"]
                threshold = constraint["threshold"]
                
                if operator == ">" and avg_metrics[metric] <= threshold:
                    constraints_satisfied = False
                elif operator == ">=" and avg_metrics[metric] < threshold:
                    constraints_satisfied = False
                elif operator == "<" and avg_metrics[metric] >= threshold:
                    constraints_satisfied = False
                elif operator == "<=" and avg_metrics[metric] > threshold:
                    constraints_satisfied = False
            
            # Jika semua constraint terpenuhi, evaluasi objective function
            if constraints_satisfied:
                objective_metric = objective_function["metric"]
                objective_value = avg_metrics[objective_metric]
                
                is_better = False
                if objective_function["direction"] == "maximize" and objective_value > best_score:
                    is_better = True
                elif objective_function["direction"] == "minimize" and objective_value < best_score:
                    is_better = True
                
                if is_better:
                    best_score = objective_value
                    best_solution = {
                        "doctor_config": doctor_config,
                        "scheduling_strategy": strategy,
                        "metrics": avg_metrics
                    }
            
            # Tambahkan hasil ke daftar untuk visualisasi
            results.append({
                "doctor_config": str(doctor_config),
                "scheduling_strategy": strategy,
                **avg_metrics,
                "constraints_satisfied": constraints_satisfied
            })
    
    # Buat DataFrame untuk analisis
    results_df = pd.DataFrame(results)
    
    return best_solution, results_df


def plot_enhanced_results(results_df, sensitivity_results=None, optimization_results=None):
    """Visualisasi hasil simulasi yang ditingkatkan"""
    
    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 1. Visualisasi hasil sensitivitas (jika ada)
    if sensitivity_results is not None and not sensitivity_results.empty:
        unique_params = sensitivity_results['parameter'].unique()
        
        for param in unique_params:
            param_data = sensitivity_results[sensitivity_results['parameter'] == param]
            
            plt.figure(figsize=(12, 8))
            
            # Buat subplot
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            
            # Plot wait time
            axes[0].plot(param_data['value'], param_data['overall_avg_wait_time'], marker='o', linewidth=2)
            axes[0].set_xlabel(f'Parameter Value ({param})')
            axes[0].set_ylabel('Average Wait Time (minutes)')
            axes[0].set_title(f'Sensitivity: Wait Time vs {param}')
            axes[0].grid(True)
            
            # Plot utilization
            axes[1].plot(param_data['value'], param_data['overall_doctor_utilization'], marker='o', linewidth=2, color='orange')
            axes[1].set_xlabel(f'Parameter Value ({param})')
            axes[1].set_ylabel('Doctor Utilization (%)')
            axes[1].set_title(f'Sensitivity: Utilization vs {param}')
            axes[1].grid(True)
            
            # Plot service rate
            axes[2].plot(param_data['value'], param_data['service_rate'], marker='o', linewidth=2, color='green')
            axes[2].set_xlabel(f'Parameter Value ({param})')
            axes[2].set_ylabel('Service Rate (%)')
            axes[2].set_title(f'Sensitivity: Service Rate vs {param}')
            axes[2].grid(True)
            
            plt.tight_layout()
            plt.savefig(f'sensitivity_{param}.png')
            plt.close()
    
    # 2. Visualisasi hasil optimasi (jika ada)
    if optimization_results is not None and not optimization_results.empty:
        # Plot scatter hasil optimasi
        plt.figure(figsize=(10, 8))
        
        # Warna berdasarkan constraint satisfied
        colors = optimization_results['constraints_satisfied'].map({True: 'green', False: 'red'})
        
        scatter = plt.scatter(
            optimization_results['overall_doctor_utilization'],
            optimization_results['overall_avg_wait_time'],
            c=colors,
            s=100,
            alpha=0.7
        )
        
        # Tambahkan label
        for i, row in optimization_results.iterrows():
            plt.annotate(
                f"{row['scheduling_strategy']}",
                (row['overall_doctor_utilization'], row['overall_avg_wait_time']),
                textcoords="offset points",
                xytext=(0, 5),
                ha='center',
                fontsize=8
            )
        
        plt.xlabel('Doctor Utilization (%)')
        plt.ylabel('Average Wait Time (minutes)')
        plt.title('Optimization Results: Wait Time vs Utilization')
        
        # Tambahkan legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Constraints Satisfied'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Constraints Not Satisfied')
        ]
        plt.legend(handles=legend_elements)
        
        plt.grid(True)
        plt.savefig('optimization_results.png')
        plt.close()
    
    # 3. Plot distribusi waktu tunggu berdasarkan strategi penjadwalan
    if 'scheduling_strategy' in results_df.columns:
        strategies = results_df['scheduling_strategy'].unique()
        
        plt.figure(figsize=(12, 6))
        
        for i, strategy in enumerate(strategies):
            strategy_data = results_df[results_df['scheduling_strategy'] == strategy]
            plt.bar(
                i, 
                strategy_data['overall_avg_wait_time'].mean(), 
                yerr=strategy_data['overall_avg_wait_time'].std(),
                label=strategy,
                alpha=0.7
            )
        
        plt.xlabel('Scheduling Strategy')
        plt.ylabel('Average Wait Time (minutes)')
        plt.title('Wait Time by Scheduling Strategy')
        plt.xticks(range(len(strategies)), strategies)
        plt.grid(True, axis='y')
        plt.savefig('wait_time_by_strategy.png')
        plt.close()
    
    print("Enhanced plots saved to current directory.")


def main_enhanced():
    """Fungsi utama untuk simulasi klinik yang ditingkatkan"""
    # Simulasi selama 8 jam (480 menit)
    sim_time = 480  
    
    # 1. Konfigurasi dasar
    # Dokter berdasarkan spesialisasi
    doctor_config = {
        "general": 3,      # Dokter umum
        "specialist": 2,   # Spesialis
        "preventive": 1,   # Pemeriksaan rutin/preventif
        "followup": 1      # Tindak lanjut
    }
    
    # Rata-rata waktu konsultasi berdasarkan tipe pasien (dalam menit)
    mean_consult_times = {
        "emergency": 30,
        "urgent": 25,
        "regular": 20,
        "checkup": 15,
        "followup": 10,
        "cardiology": 35,
        "dermatology": 25,
        "pediatrics": 20
    }
    
    # Tingkat kedatangan pasien berdasarkan tipe (pasien per menit)
    patient_arrival_rates = {
        "emergency": 0.02,  # ~ 1.2 pasien/jam
        "urgent": 0.03,     # ~ 1.8 pasien/jam
        "regular": 0.10,    # ~ 6 pasien/jam
        "checkup": 0.05,    # ~ 3 pasien/jam
        "followup": 0.04,   # ~ 2.4 pasien/jam
        "cardiology": 0.02, # ~ 1.2 pasien/jam
        "dermatology": 0.03,# ~ 1.8 pasien/jam
        "pediatrics": 0.03  # ~ 1.8 pasien/jam
    }
    
    # Probabilitas tipe pasien
    patient_type_probabilities = {
        "emergency": 0.05,
        "urgent": 0.10,
        "regular": 0.40,
        "checkup": 0.20,
        "followup": 0.10,
        "cardiology": 0.05,
        "dermatology": 0.05,
        "pediatrics": 0.05
    }
    
    # Data historis untuk validasi (contoh)
    historical_data = {
        "avg_wait_time": {
            "emergency": 5.2,
            "urgent": 12.5,
            "regular": 25.3,
            "checkup": 18.6,
            "followup": 10.1
        },
        "avg_service_time": {
            "emergency": 32.1,
            "urgent": 24.9,
            "regular": 19.8,
            "checkup": 16.2,
            "followup": 9.8
        },
        "doctor_utilization": {
            "general": 75.3,
            "specialist": 68.4,
            "preventive": 62.8,
            "followup": 58.2
        }
    }
    
    # 2. Validasi model dengan data historis
    print("\n=== VALIDASI MODEL ===")
    validation_result, _ = run_enhanced_simulation(
        doctor_config=doctor_config,
        mean_consult_times=mean_consult_times,
        patient_arrival_rates=patient_arrival_rates,
        patient_type_probabilities=patient_type_probabilities,
        historical_data=historical_data,
        sim_time=sim_time
    )
    
    print(f"Model valid: {validation_result['validation']['valid']}")
    for metric, results in validation_result['validation']['results'].items():
        print(f"  {metric}: {results['mean_error_percent']:.2f}% error")
    
    # 3. Analisis sensitivitas
    print("\n=== ANALISIS SENSITIVITAS ===")
    # Parameter yang akan dianalisis
    param_ranges = {
        # Variasi jumlah dokter
        "doctor_config": [
            {"general": 2, "specialist": 2, "preventive": 1, "followup": 1},
            {"general": 3, "specialist": 2, "preventive": 1, "followup": 1},
            {"general": 4, "specialist": 2, "preventive": 1, "followup": 1},
            {"general": 3, "specialist": 3, "preventive": 1, "followup": 1},
            {"general": 3, "specialist": 2, "preventive": 2, "followup": 1}
        ],
        # Strategi penjadwalan
        "scheduling_strategy": ["fifo", "priority", "type_based"],
        # Faktor untuk arrival rate (untuk melihat pengaruh volume pasien)
        "patient_arrival_rates": [0.8, 0.9, 1.0, 1.1, 1.2]
    }
    
# Parameter tetap
    fixed_params = {
        "doctor_config": doctor_config,
        "mean_consult_times": mean_consult_times,
        "patient_arrival_rates": patient_arrival_rates,
        "patient_type_probabilities": patient_type_probabilities,
        "scheduling_strategy": "fifo",
        "historical_data": historical_data
    }
    
    sensitivity_results = sensitivity_analysis(param_ranges, fixed_params, sim_time)
    
    # 4. Optimasi parameter
    print("\n=== OPTIMASI PARAMETER ===")
    # Parameter space untuk optimasi
    param_space = {
        "doctor_config": [
            {"general": 2, "specialist": 2, "preventive": 1, "followup": 1},
            {"general": 3, "specialist": 2, "preventive": 1, "followup": 1},
            {"general": 4, "specialist": 2, "preventive": 1, "followup": 1},
            {"general": 3, "specialist": 3, "preventive": 1, "followup": 1},  # Added configuration
            {"general": 4, "specialist": 3, "preventive": 1, "followup": 1},  # Added configuration
            {"general": 3, "specialist": 2, "preventive": 2, "followup": 1}   # Added configuration
            ],
        "scheduling_strategy": ["fifo", "priority", "type_based"],
        "mean_consult_times": [mean_consult_times],
        "patient_arrival_rates": [patient_arrival_rates],
        "patient_type_probabilities": [patient_type_probabilities]
    }
    
    # Objective function: minimize average wait time
    objective_function = {
        "metric": "overall_avg_wait_time",
        "direction": "minimize"
    }
    
    # Constraints
    constraints = [
        {
            "metric": "overall_doctor_utilization",
            "operator": ">=",
            "threshold": 65  # Minimum 70% utilisasi
        },
        {
            "metric": "service_rate",
            "operator": ">=",
            "threshold": 90  # Minimum 95% tingkat layanan
        }
    ]
    
    best_solution, optimization_results = optimize_parameters(
        param_space, objective_function, constraints, sim_time
    )

    # Add a check before trying to print the solution
    if best_solution is None:
        print("\nNo solution found that satisfies all constraints.")
        print("Consider relaxing your constraints or expanding the parameter space.")
        
        # Optionally, find the closest solution by filtering results
        if not optimization_results.empty:
            print("\nBest available solutions (may not meet all constraints):")
            # Sort by the objective function (assuming minimizing wait time)
            sorted_results = optimization_results.sort_values('overall_avg_wait_time')
            print(sorted_results.head(3))
    else:
        print("\nSolusi Optimal:")
        print(f"Konfigurasi Dokter: {best_solution['doctor_config']}")
        print(f"Strategi Penjadwalan: {best_solution['scheduling_strategy']}")
        print("\nMetrik Kinerja:")
        print(f"Rata-rata Waktu Tunggu: {best_solution['metrics']['overall_avg_wait_time']:.2f} menit")
        print(f"Utilisasi Dokter: {best_solution['metrics']['overall_doctor_utilization']:.2f}%")
        print(f"Tingkat Layanan: {best_solution['metrics']['service_rate']:.2f}%")
        
    # 5. Visualisasi hasil
    print("\n=== VISUALISASI HASIL ===")
    plot_enhanced_results(optimization_results, sensitivity_results)

if __name__ == "__main__":
    main_enhanced()