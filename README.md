# Simulasi Antrian Call Centre

## Deskripsi
Repositori ini berisi proyek Pemodelan dan Simulasi Data yang bertujuan untuk menganalisis dan mengoptimalkan sistem antrian di call centre menggunakan dataset `simulated_call_centre.csv`. Simulasi ini dilakukan untuk menentukan jumlah agen optimal serta memahami performa sistem berdasarkan berbagai parameter.

## Instalasi dan Dependensi
Sebelum menjalankan proyek ini, pastikan Anda telah menginstal pustaka yang diperlukan:
```bash
pip install pandas numpy matplotlib seaborn scipy
```

## Langkah-langkah Simulasi
1. **Load dan Eksplorasi Dataset**
   - Membaca file CSV `simulated_call_centre.csv`
   - Menganalisis pola kedatangan panggilan dan distribusi waktu layanan
2. **Simulasi Antrian**
   - Menentukan distribusi terbaik untuk waktu antar kedatangan dan waktu layanan
   - Implementasi model antrian M/M/c untuk menentukan jumlah agen optimal
3. **Analisis Performa**
   - Mengevaluasi metrik seperti waktu tunggu, service level, dan utilization
   - Menentukan jumlah agen optimal
4. **Optimasi dan Rekomendasi**
   - Menganalisis dampak perubahan jumlah agen terhadap performa sistem
   
## Ringkasan Hasil Simulasi dan Analisis
1. **Jumlah agen optimal:** 269.0
2. **Service level dengan agen optimal:** 100.00%
3. **Waktu tunggu rata-rata dengan agen optimal:** 0.00 detik
4. **Utilization agen dengan agen optimal:** 84.01%

## Rekomendasi
1. Alokasikan agen sesuai dengan pola kedatangan panggilan per jam.
2. Pertimbangkan untuk meningkatkan jumlah agen pada jam sibuk.
3. Evaluasi upaya untuk mengurangi waktu layanan rata-rata.
4. Pantau utilization agen untuk memastikan efisiensi dan pencegahan burnout.

## Cara Menjalankan Kode
1. Clone repository ini ke komputer Anda:
   ```bash
   git clone https://github.com/reddishowo/data-modelling-simulation.git
   cd repo-name
   ```
2. Pastikan semua dependensi telah terinstal.
3. Jalankan Jupyter Notebook dan buka file `.ipynb` untuk menjalankan simulasi:
   ```bash
   jupyter notebook
   ```

---
