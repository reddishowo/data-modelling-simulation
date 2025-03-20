# Simulasi Antrian Bank dengan Discrete Event Simulation (DES)

## Gambaran Umum

Proyek ini merupakan simulasi antrian bank yang dibangun menggunakan pendekatan *Discrete Event Simulation* (DES) dengan bahasa pemrograman Python. Simulasi ini bertujuan untuk menganalisis performa sistem antrian bank berdasarkan beberapa skenario, seperti jumlah teller, tingkat kedatangan pelanggan pada jam sibuk, utilisasi teller, dan implementasi antrian prioritas untuk pelanggan VIP. Proyek ini dirancang untuk memberikan wawasan tentang dinamika antrian bank melalui statistik dan visualisasi yang rinci.

Simulasi ini mencakup elemen kompleks seperti waktu layanan yang bervariasi berdasarkan kompleksitas transaksi pelanggan, jadwal istirahat teller, dan simulasi multi-hari. Hasil simulasi divisualisasikan dalam bentuk grafik untuk mempermudah analisis performa sistem.

## Fitur Utama

- **Simulasi Multi-Skenario**:
  - Mengubah jumlah teller (2 atau 3 teller).
  - Mensimulasikan jam sibuk dengan meningkatkan tingkat kedatangan pelanggan (`peak_hour_factor`).
  - Berjalan selama 5 hari, dengan setiap hari memiliki durasi 8 jam (480 menit).

- **Antrian Prioritas**:
  - Pelanggan dibagi menjadi VIP (20%) dan reguler (80%).
  - Pelanggan VIP diprioritaskan dalam antrian, sehingga dilayani lebih dulu.

- **Kompleksitas Transaksi**:
  - Waktu layanan pelanggan bervariasi berdasarkan tingkat kompleksitas transaksi (sederhana, sedang, kompleks) menggunakan distribusi Gamma.

- **Jadwal Istirahat Teller**:
  - Teller mengambil istirahat secara acak setiap ~2 jam, dengan durasi istirahat 10-20 menit, yang memengaruhi ketersediaan mereka untuk melayani pelanggan.

- **Statistik Rinci**:
  - Melacak waktu tunggu terpisah untuk pelanggan VIP dan reguler.
  - Mencatat panjang antrian maksimum.
  - Menghitung utilisasi rata-rata dan per teller.

- **Visualisasi**:
  - Distribusi waktu tunggu (VIP vs reguler) menggunakan KDE plot.
  - Utilisasi teller dan panjang antrian dari waktu ke waktu menggunakan plot garis.
  - Boxplot waktu tunggu untuk membandingkan skenario.
  - Heatmap utilisasi teller per skenario, dipisahkan berdasarkan jumlah teller.

## Prasyarat

Untuk menjalankan proyek ini, pastikan Anda memiliki:
- Python 3.6 atau lebih tinggi.
- Library Python berikut:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `scipy`

Anda dapat menginstal library tersebut menggunakan perintah berikut:
```bash
pip install numpy pandas matplotlib seaborn scipy
```

## Cara Menjalankan

1. **Clone atau Unduh Proyek**:
   Clone repositori ini atau unduh file proyek ke komputer Anda.

2. **Buka di Jupyter Notebook**:
   - Pastikan Anda memiliki Jupyter Notebook terinstal (`pip install jupyter`).
   - Buka terminal dan navigasikan ke direktori proyek.
   - Jalankan perintah:
     ```bash
     jupyter notebook
     ```
   - Buka file `bank_queue_simulation.ipynb` di browser.

3. **Jalankan Seluruh Sel**:
   - Jalankan semua sel dalam notebook untuk menjalankan simulasi dan menghasilkan visualisasi.
   - Simulasi akan berjalan untuk 4 skenario:
     - 2 teller, kondisi normal.
     - 3 teller, kondisi normal.
     - 2 teller, jam sibuk.
     - 3 teller, jam sibuk.

4. **Lihat Hasil**:
   - Statistik simulasi akan ditampilkan di output.
   - Visualisasi akan muncul sebagai grafik (KDE plot, plot garis, boxplot, dan heatmap).

## Struktur Kode

- **Kelas `Event`**:
  - Mengelola peristiwa dalam simulasi, seperti kedatangan (`arrival`), keberangkatan (`departure`), teller mulai istirahat (`break_start`), dan selesai istirahat (`break_end`).

- **Kelas `Customer`**:
  - Menyimpan informasi pelanggan, termasuk waktu kedatangan, status VIP, kompleksitas transaksi, waktu mulai layanan, dan waktu keberangkatan.

- **Kelas `Teller`**:
  - Mengelola status teller (sibuk atau istirahat), waktu sibuk, dan jadwal istirahat.

- **Fungsi `bank_simulation`**:
  - Fungsi utama yang menjalankan simulasi DES.
  - Parameter:
    - `num_tellers`: Jumlah teller (default: 2 atau 3).
    - `peak_hour_factor`: Faktor untuk meningkatkan tingkat kedatangan pada jam sibuk (default: 1.0 untuk normal, 2.0 untuk jam sibuk).
    - `sim_days`: Jumlah hari simulasi (default: 5).
    - `vip_ratio`: Proporsi pelanggan VIP (default: 0.2).
    - `break_freq`: Frekuensi istirahat teller (default: 120 menit).
  - Mengembalikan statistik seperti waktu tunggu, utilisasi, dan panjang antrian.

- **Bagian Visualisasi**:
  - Menghasilkan 4 visualisasi utama untuk menganalisis performa sistem.

## Contoh Hasil

Berikut adalah ringkasan statistik dari simulasi:

- **2 Tellers, Normal**:
  - Rata-rata Waktu Tunggu VIP: 1.05 menit
  - Rata-rata Waktu Tunggu Regular: 3.98 menit
  - Panjang Antrian Maksimum: 8
  - Rata-rata Utilisasi: 65.82%
  - Utilisasi per Teller: ['73.03%', '58.86%']

- **3 Tellers, Normal**:
  - Rata-rata Waktu Tunggu VIP: 0.19 menit
  - Rata-rata Waktu Tunggu Regular: 0.35 menit
  - Panjang Antrian Maksimum: 4
  - Rata-rata Utilisasi: 37.25%
  - Utilisasi per Teller: ['58.74%', '38.70%', '20.28%']

- **2 Tellers, Peak**:
  - Rata-rata Waktu Tunggu VIP: 3.17 menit
  - Rata-rata Waktu Tunggu Regular: 339.66 menit
  - Panjang Antrian Maksimum: 218
  - Rata-rata Utilisasi: 99.59%
  - Utilisasi per Teller: ['99.93%', '99.85%']

- **3 Tellers, Peak**:
  - Rata-rata Waktu Tunggu VIP: 1.39 menit
  - Rata-rata Waktu Tunggu Regular: 6.19 menit
  - Panjang Antrian Maksimum: 16
  - Rata-rata Utilisasi: 84.93%
  - Utilisasi per Teller: ['88.68%', '85.59%', '78.24%']

Visualisasi mencakup:
- Distribusi waktu tunggu (VIP vs reguler).
- Utilisasi teller dan panjang antrian dari waktu ke waktu.
- Boxplot waktu tunggu per skenario.
- Heatmap utilisasi teller per skenario.

## Pengembangan Lebih Lanjut

- Menambahkan faktor seperti tingkat kepuasan pelanggan atau biaya operasional teller.
- Mengimplementasikan skenario dengan lebih banyak teller atau variasi jadwal operasional.
- Menambahkan analisis sensitivitas untuk parameter seperti `vip_ratio` atau `break_freq`.

