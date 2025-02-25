# Simulasi Sistem Antrean Layanan Digital

## Validasi Model
Model saat ini **tidak valid** berdasarkan perbandingan metrik simulasi dengan data referensi:
- **Rata-rata Waktu Tunggu:** 79.97% error
- **Rata-rata Waktu Pelayanan:** 21.74% error
- **Utilisasi Dokter:** 93.59% error

## Analisis Sensitivitas
Eksperimen dilakukan dengan berbagai konfigurasi jumlah dokter, strategi penjadwalan, dan tingkat kedatangan pasien.

### Variasi `doctor_config`
| General | Specialist | Preventive | Follow-up | Avg. Wait Time (min) | Doctor Utilization (%) | Service Rate (%) |
|---------|------------|------------|-----------|----------------------|------------------------|------------------|
| 2       | 2          | 1          | 1         | 1.24                 | 10.55                   | 89.13            |
| 3       | 2          | 1          | 1         | 0.54                 | 10.30                   | 91.62            |
| 4       | 2          | 1          | 1         | 0.30                 | 10.11                   | 98.10            |
| 3       | 3          | 1          | 1         | 1.39                 | 9.06                    | 94.70            |
| 3       | 2          | 2          | 1         | 3.94                 | 9.43                    | 90.43            |

### Variasi `scheduling_strategy`
| Strategy  | Avg. Wait Time (min) | Doctor Utilization (%) | Service Rate (%) |
|-----------|----------------------|------------------------|------------------|
| FIFO      | 0.97                 | 9.41                   | 82.35            |
| Priority  | 1.19                 | 10.06                   | 91.19            |
| Type-based | 1.13                 | 9.56                    | 83.78            |

### Variasi `patient_arrival_rates`
| Arrival Rate | Avg. Wait Time (min) | Doctor Utilization (%) | Service Rate (%) |
|-------------|----------------------|------------------------|------------------|
| 0.8         | 0.51                 | 6.71                    | 95.84            |
| 0.9         | 0.35                 | 6.28                    | 86.06            |
| 1.0         | 0.44                 | 6.08                    | 94.65            |
| 1.1         | 1.22                 | 8.36                    | 93.73            |
| 1.2         | 3.13                 | 10.32                   | 95.68            |

## Optimasi Parameter
Dari total 18 kombinasi parameter yang dievaluasi, tidak ada solusi yang memenuhi semua batasan. **Solusi terbaik yang tersedia** (namun masih melanggar batasan) adalah:

| Doctor Config | Scheduling Strategy | Avg. Wait Time (min) | Doctor Utilization (%) | Service Rate (%) | Constraints Met |
|--------------|--------------------|----------------------|------------------------|------------------|----------------|
| `{'general': 4, 'specialist': 3, 'preventive': 1, 'followup': 1}` | Type-based | 0.00 | 4.69 | 91.91 | ❌ |
| `{'general': 2, 'specialist': 2, 'preventive': 1, 'followup': 1}` | Priority | 0.06 | 11.69 | 91.53 | ❌ |
| `{'general': 3, 'specialist': 3, 'preventive': 1, 'followup': 1}` | Type-based | 0.16 | 7.62 | 88.96 | ❌ |

## Kesimpulan & Rekomendasi
- Model saat ini memiliki kesalahan besar dalam metrik validasi, sehingga perlu diperbaiki.
- Sensitivitas menunjukkan bahwa peningkatan jumlah dokter dan strategi penjadwalan memengaruhi waktu tunggu dan utilisasi.
- Tidak ditemukan konfigurasi parameter yang memenuhi semua batasan. Disarankan untuk melonggarkan batasan atau memperluas ruang parameter.

### Langkah Selanjutnya
1. **Validasi ulang model** dengan parameter yang lebih realistis.
2. **Eksperimen lebih lanjut** untuk menemukan parameter yang lebih optimal.
3. **Pertimbangkan faktor lain** seperti distribusi kedatangan pasien yang lebih kompleks.
4. **Gunakan data historis** untuk kalibrasi lebih lanjut terhadap model.

