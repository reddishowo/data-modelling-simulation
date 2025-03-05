# Simulasi Monte Carlo untuk Mengestimasi Nilai Pi (π)

Repository ini berisi implementasi metode Monte Carlo untuk mengestimasi nilai Pi menggunakan teknik sampling acak. Proyek ini merupakan bagian dari tugas mata kuliah Pemodelan dan Simulasi Data.

## Deskripsi

Metode Monte Carlo adalah teknik komputasi yang memanfaatkan pengambilan sampel acak untuk mendapatkan hasil numerik. Dalam proyek ini, metode Monte Carlo digunakan untuk mengestimasi nilai konstanta matematika Pi (π = 3.14159...) dengan memanfaatkan hubungan geometris antara lingkaran dan persegi.

Prinsip dasarnya adalah:
1. Membangkitkan titik-titik acak dalam persegi dengan rentang [0,1] × [0,1]
2. Menghitung berapa banyak titik yang jatuh dalam seperempat lingkaran dengan pusat (0,0) dan jari-jari 1
3. Menggunakan rasio titik dalam lingkaran terhadap total titik untuk mengestimasi nilai π

## Fitur

- Implementasi simulasi Monte Carlo dengan jumlah titik yang dapat dikonfigurasi
- Visualisasi sebaran titik-titik acak dengan perbedaan warna untuk titik di dalam dan di luar lingkaran
- Analisis hubungan antara jumlah titik, akurasi estimasi, dan waktu komputasi
- Visualisasi error dan konvergensi estimasi π terhadap jumlah titik

## Contoh Hasil

Proyek ini menghasilkan dua gambar utama:
1. Visualisasi titik-titik acak pada kuadrat dengan pewarnaan berbeda untuk titik di dalam dan di luar lingkaran
2. Grafik yang menunjukkan hubungan antara jumlah titik dengan error dan estimasi nilai π

## Penggunaan

```python
# Menjalankan simulasi untuk 100,000 titik
num_points = 100000
pi_estimate, x, y, distances = monte_carlo_pi(num_points)

# Menampilkan hasil
print(f"Estimasi nilai π dengan {num_points} titik: {pi_estimate}")
print(f"Nilai π sebenarnya: {np.pi}")
print(f"Error: {abs(pi_estimate - np.pi)}")

# Visualisasi hasil
fig = visualize_simulation(x, y, distances, num_points)
plt.show()

# Menjalankan eksperimen dengan berbagai jumlah titik
points_list, pi_estimates, errors, execution_times = run_pi_experiment(max_points=1000000, num_steps=10)
```

## Persyaratan

Proyek ini memerlukan dependensi berikut:
- Python 3.x
- NumPy
- Matplotlib

Instalasi dependensi dapat dilakukan dengan perintah:
```
pip install numpy matplotlib
```

## Struktur Proyek

```
monte_carlo_pi/
│
├── monte_carlo_pi.py          # Implementasi metode Monte Carlo
├── monte_carlo_pi_visualization.png  # Visualisasi titik-titik acak
├── monte_carlo_pi_results.png # Grafik error dan estimasi Pi
└── README.md                  # Dokumentasi proyek
```

## Hasil Analisis

Analisis hasil menunjukkan bahwa:
1. Error estimasi menurun dengan laju O(1/√n) di mana n adalah jumlah titik
2. Untuk mendapatkan presisi yang lebih tinggi, diperlukan peningkatan jumlah titik secara signifikan
3. Metode Monte Carlo efektif untuk demonstrasi dan pembelajaran, meskipun bukan metode tercepat untuk menghitung π

