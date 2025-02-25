import simpy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

class ClinicReservationSystem:
    def __init__(self, env, num_doctors, mean_consult_time, patient_arrival_rate):
        self.env = env
        self.doctors = simpy.Resource(env, capacity=num_doctors)
        self.mean_consult_time = mean_consult_time
        self.patient_arrival_rate = patient_arrival_rate
        
        # Statistik
        self.waiting_times = []
        self.service_times = []
        self.queue_lengths = []
        self.doctor_busy_time = 0
        self.last_queue_length_update = 0
        self.last_queue_length = 0
        
        # Monitor antrian setiap menit
        env.process(self.monitor_queue())
    
    def monitor_queue(self):
        while True:
            # Catat panjang antrian saat ini
            current_time = self.env.now
            time_diff = current_time - self.last_queue_length_update
            
            # Tambahkan panjang antrian sebelumnya ke list, berdasarkan waktu berlalu
            if time_diff > 0:
                self.queue_lengths.extend([self.last_queue_length] * int(time_diff))
            
            # Update nilai terakhir
            self.last_queue_length = len(self.doctors.queue)
            self.last_queue_length_update = current_time
            
            # Tunggu 1 unit waktu
            yield self.env.timeout(1)
    
    def patient_arrival(self, patient_id):
        # Catat waktu kedatangan
        arrival_time = self.env.now
        
        # Request dokter
        with self.doctors.request() as request:
            # Tunggu sampai dokter tersedia
            yield request
            
            # Dokter tersedia, catat waktu tunggu
            wait_time = self.env.now - arrival_time
            self.waiting_times.append(wait_time)
            
            # Lakukan konsultasi
            # Waktu konsultasi mengikuti distribusi eksponensial
            consult_time = random.expovariate(1.0 / self.mean_consult_time)
            self.service_times.append(consult_time)
            
            # Track waktu dokter sibuk
            self.doctor_busy_time += consult_time
            
            # Simulasikan waktu konsultasi
            yield self.env.timeout(consult_time)
            

def generate_patients(env, system):
    # Generate pasien berdasarkan distribusi Poisson
    patient_id = 0
    while True:
        # Waktu antar kedatangan mengikuti distribusi eksponensial
        interarrival_time = random.expovariate(system.patient_arrival_rate)
        yield env.timeout(interarrival_time)
        
        # Pasien baru tiba
        patient_id += 1
        env.process(system.patient_arrival(patient_id))

def run_simulation(num_doctors, mean_consult_time, patient_arrival_rate, sim_time=480):
    # Buat lingkungan simulasi baru
    env = simpy.Environment()
    
    # Buat sistem reservasi klinik
    system = ClinicReservationSystem(env, num_doctors, mean_consult_time, patient_arrival_rate)
    
    # Mulai proses kedatangan pasien
    env.process(generate_patients(env, system))
    
    # Jalankan simulasi
    env.run(until=sim_time)
    
    # Hitung statistik
    avg_wait_time = np.mean(system.waiting_times) if system.waiting_times else 0
    avg_service_time = np.mean(system.service_times) if system.service_times else 0
    avg_queue_length = np.mean(system.queue_lengths) if system.queue_lengths else 0
    doctor_utilization = system.doctor_busy_time / (sim_time * num_doctors) * 100
    
    # Kumpulkan hasil
    results = {
        "num_doctors": num_doctors,
        "patient_arrival_rate": patient_arrival_rate,
        "mean_consult_time": mean_consult_time,
        "total_patients": len(system.waiting_times),
        "avg_wait_time": avg_wait_time,
        "avg_service_time": avg_service_time,
        "avg_queue_length": avg_queue_length,
        "doctor_utilization": doctor_utilization,
        "all_waiting_times": system.waiting_times
    }
    
    return results

def main():
    # Parameter simulasi
    sim_time = 480  # Simulasi selama 8 jam (480 menit)
    mean_consult_time = 20  # Rata-rata waktu konsultasi 20 menit
    doctor_counts = [1, 2, 3, 4, 5]  # Variasi jumlah dokter
    arrival_rates = [0.1, 0.15, 0.2, 0.25, 0.3]  # Pasien per menit (6-18 pasien per jam)
    
    # Hasil simulasi
    all_results = []
    
    # Jalankan simulasi untuk setiap kombinasi parameter
    for num_doctors in doctor_counts:
        for arrival_rate in arrival_rates:
            # Jalankan simulasi dengan 5 replikasi
            replication_results = []
            for rep in range(5):
                result = run_simulation(num_doctors, mean_consult_time, arrival_rate, sim_time)
                replication_results.append(result)
            
            # Hitung rata-rata dari 5 replikasi
            avg_result = {
                "num_doctors": num_doctors,
                "patient_arrival_rate": arrival_rate,
                "mean_consult_time": mean_consult_time,
                "total_patients": np.mean([r["total_patients"] for r in replication_results]),
                "avg_wait_time": np.mean([r["avg_wait_time"] for r in replication_results]),
                "avg_service_time": np.mean([r["avg_service_time"] for r in replication_results]),
                "avg_queue_length": np.mean([r["avg_queue_length"] for r in replication_results]),
                "doctor_utilization": np.mean([r["doctor_utilization"] for r in replication_results]),
            }
            
            all_results.append(avg_result)
            
            print(f"Doctors: {num_doctors}, Arrival Rate: {arrival_rate:.2f} patients/min")
            print(f"  Total Patients: {avg_result['total_patients']:.1f}")
            print(f"  Average Wait Time: {avg_result['avg_wait_time']:.2f} minutes")
            print(f"  Average Queue Length: {avg_result['avg_queue_length']:.2f} patients")
            print(f"  Doctor Utilization: {avg_result['doctor_utilization']:.2f}%")
            print("-" * 50)
    
    # Konversi ke DataFrame untuk analisis lebih lanjut
    results_df = pd.DataFrame(all_results)
    
    # Visualisasi hasil
    plot_results(results_df)
    
    return results_df

def plot_results(results_df):
    # 1. Plot waktu tunggu rata-rata vs jumlah dokter untuk setiap arrival rate
    plt.figure(figsize=(10, 6))
    for rate in results_df['patient_arrival_rate'].unique():
        subset = results_df[results_df['patient_arrival_rate'] == rate]
        plt.plot(subset['num_doctors'], subset['avg_wait_time'], marker='o', 
                 label=f'Arrival Rate: {rate:.2f} patients/min')
    
    plt.xlabel('Number of Doctors')
    plt.ylabel('Average Wait Time (minutes)')
    plt.title('Average Wait Time vs Number of Doctors')
    plt.grid(True)
    plt.legend()
    plt.savefig('wait_time_vs_doctors.png')
    
    # 2. Plot utilisasi dokter vs jumlah dokter untuk setiap arrival rate
    plt.figure(figsize=(10, 6))
    for rate in results_df['patient_arrival_rate'].unique():
        subset = results_df[results_df['patient_arrival_rate'] == rate]
        plt.plot(subset['num_doctors'], subset['doctor_utilization'], marker='o', 
                 label=f'Arrival Rate: {rate:.2f} patients/min')
    
    plt.xlabel('Number of Doctors')
    plt.ylabel('Doctor Utilization (%)')
    plt.title('Doctor Utilization vs Number of Doctors')
    plt.grid(True)
    plt.legend()
    plt.savefig('utilization_vs_doctors.png')
    
    # 3. Plot panjang antrian rata-rata vs jumlah dokter untuk setiap arrival rate
    plt.figure(figsize=(10, 6))
    for rate in results_df['patient_arrival_rate'].unique():
        subset = results_df[results_df['patient_arrival_rate'] == rate]
        plt.plot(subset['num_doctors'], subset['avg_queue_length'], marker='o', 
                 label=f'Arrival Rate: {rate:.2f} patients/min')
    
    plt.xlabel('Number of Doctors')
    plt.ylabel('Average Queue Length (patients)')
    plt.title('Average Queue Length vs Number of Doctors')
    plt.grid(True)
    plt.legend()
    plt.savefig('queue_length_vs_doctors.png')
    
    # 4. Tampilkan hubungan trade-off antara waktu tunggu dan utilisasi dokter
    plt.figure(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(results_df['patient_arrival_rate'].unique())))
    
    for i, rate in enumerate(results_df['patient_arrival_rate'].unique()):
        subset = results_df[results_df['patient_arrival_rate'] == rate]
        plt.scatter(subset['doctor_utilization'], subset['avg_wait_time'], 
                   label=f'Arrival Rate: {rate:.2f}', color=colors[i], s=100)
        
        # Tambahkan anotasi jumlah dokter
        for _, row in subset.iterrows():
            plt.annotate(f"{int(row['num_doctors'])}", 
                        (row['doctor_utilization'], row['avg_wait_time']),
                        textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.xlabel('Doctor Utilization (%)')
    plt.ylabel('Average Wait Time (minutes)')
    plt.title('Trade-off: Wait Time vs Utilization')
    plt.grid(True)
    plt.legend()
    plt.savefig('tradeoff_wait_vs_utilization.png')
    
    print("Plots saved to current directory.")

if __name__ == "__main__":
    results_df = main()
    # Save results to CSV for further analysis
    results_df.to_csv('clinic_simulation_results.csv', index=False)
    print("Results saved to clinic_simulation_results.csv")
