# Simulasi Sistem Reservasi Online Klinik Kesehatan.

## Deskripsi Proyek
Proyek ini bertujuan untuk mensimulasikan sistem antrean dalam sebuah platform layanan digital menggunakan **SimPy**, sebuah pustaka Python untuk simulasi berbasis proses. 

## Parameter Simulasi
Simulasi ini mencakup beberapa variabel penting, yaitu:

- **Dokter**: Jumlah dokter yang tersedia untuk melayani pasien.
- **Total Pasien**: Jumlah keseluruhan pasien yang telah mendapatkan layanan.
- **Waktu Tunggu Rata-rata**: Waktu rata-rata yang dihabiskan pasien dalam antrean sebelum mendapatkan pelayanan medis (dalam menit).
- **Panjang Antrean Rata-rata**: Rata-rata jumlah pasien yang sedang menunggu dalam antrean.
- **Utilisasi Dokter**: Persentase waktu kerja dokter yang digunakan untuk melayani pasien dibandingkan dengan waktu yang tersedia.
- **Durasi Simulasi:** 8 jam (480 menit) dan 12 jam (720 menit)
- **Tingkat Kedatangan Pasien:** 0.10 hingga 0.30 pasien per menit

## Ringkasan Hasil Simulasi
Simulasi dilakukan dengan variasi jumlah dokter (1 dan 5 dokter) dan tingkat kedatangan pasien (0.10 hingga 0.30 pasien/menit). Hasil dari simulasi ini dirangkum dalam tabel berikut:

### Dibawah ini merupakan Ringkasan Hasil Simulasi menggunakan Waktu Simulasi 480 Menit atau 8 Jam

### **1 Dokter**
| Tingkat Kedatangan | Total Pasien | Waktu Tunggu (menit) | Panjang Antrean | Utilisasi (%) |
|------------------|-------------|------------------|----------------|--------------|
| 0.10 | 27.2 | 99.22 | 9.72 | 94.46 |
| 0.15 | 26.6 | 132.70 | 22.37 | 100.24 |
| 0.20 | 28.0 | 171.40 | 32.54 | 103.75 |
| 0.25 | 26.8 | 188.55 | 47.81 | 103.38 |
| 0.30 | 23.4 | 183.38 | 61.05 | 107.37 |

Dapat dilihat bahwa ketika hanya ada satu dokter, waktu tunggu meningkat secara signifikan dengan bertambahnya jumlah pasien.

### **5 Dokter**
| Tingkat Kedatangan | Total Pasien | Waktu Tunggu (menit) | Panjang Antrean | Utilisasi (%) |
|------------------|-------------|------------------|----------------|--------------|
| 0.10 | 49.0 | 0.53 | 0.06 | 38.81 |
| 0.15 | 75.4 | 2.91 | 0.48 | 69.11 |
| 0.20 | 95.8 | 4.68 | 0.99 | 80.47 |
| 0.25 | 112.6 | 17.59 | 4.46 | 89.65 |
| 0.30 | 119.2 | 47.30 | 13.48 | 100.30 |

Dapat dilihat jika dokter ditambah hingga lima orang, itu bisa mengurangi antrean secara signifikan.

## Analisis Hasil Simulasi

### 1. Pengaruh Jumlah Dokter
- **Dokter 1:**
  - Dengan tingkat kedatangan yang lebih tinggi (>0.15 pasien/menit), antrean menjadi sangat panjang dengan waktu tunggu rata-rata lebih dari 100 menit.
  - Utilisasi dokter sering kali melebihi 100%, menandakan adanya kepadatan yang menyebabkan sistem tidak mampu menangani semua pasien dengan baik.
- **Dokter 5:**
  - Waktu tunggu berkurang secara signifikan.
  - Pada tingkat kedatangan rendah (0.10 - 0.20), hampir tidak ada antrean.
  - Pada tingkat kedatangan tinggi (0.30), dokter masih dapat menangani pasien dengan waktu tunggu yang lebih masuk akal.

### 2. Perbandingan Simulasi 8 Jam vs 12 Jam
- **8 Jam:**
  - Waktu tunggu lebih rendah dibandingkan simulasi 12 jam dalam skenario dengan tingkat kedatangan yang sama, tetapi antrean tetap tinggi untuk jumlah dokter yang lebih sedikit.
  - Pada dokter 1 dan 2, antrean tetap menumpuk, sedangkan dokter 3-5 lebih mampu menangani pasien.
- **12 Jam:**
  - Waktu tunggu rata-rata meningkat, terutama dengan 1-2 dokter, menunjukkan efek akumulasi antrean dalam periode yang lebih panjang.
  - Jumlah total pasien yang ditangani meningkat, tetapi tanpa peningkatan jumlah dokter, sistem tetap mengalami kepadatan.
  - Dengan 3-5 dokter, antrean lebih terkendali, meskipun pada tingkat kedatangan tinggi, masih ada antrean yang cukup panjang.


## Analisis dan Kesimpulan
1. Jika jumlah dokter tidak mencukupi untuk menangani pasien yang datang, waktu tunggu meningkat drastis.
2. Namun, terlalu banyak dokter tanpa permintaan pasien yang tinggi menyebabkan kurangnya efisiensi pemanfaatan dokter.
3. Jika utilisasi dokter melebihi 100%, artinya kapasitas sistem telah terlampaui, yang dapat menyebabkan penurunan kualitas layanan.
4. Untuk setiap tingkat kedatangan, ada jumlah dokter optimal yang meminimalkan antrean dan tetap mempertahankan efisiensi tinggi.
5. Menambah jumlah dokter sangat berpengaruh dalam mengurangi waktu tunggu pasien dan panjang antrean.
6. Pada tingkat kedatangan tinggi, minimal 3-4 dokter diperlukan agar antrean tetap terkendali.
7. Durasi simulasi yang lebih lama menunjukkan bahwa tanpa perubahan kapasitas, antrean akan semakin panjang seiring waktu.
8. Untuk klinik dengan tingkat kedatangan tinggi, menambah dokter atau meningkatkan efisiensi pelayanan sangat penting untuk menghindari waktu tunggu yang terlalu lama.


