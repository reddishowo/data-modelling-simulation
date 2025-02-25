Simulasi Sistem Reservasi Online Klinik Kesehatan.

## Deskripsi Proyek
Proyek ini bertujuan untuk mensimulasikan sistem antrean dalam sebuah platform layanan digital menggunakan **SimPy**, sebuah pustaka Python untuk simulasi berbasis proses. 

## Parameter Simulasi
Simulasi ini mencakup beberapa variabel penting, yaitu:

- **Dokter**: Jumlah dokter yang tersedia untuk melayani pasien.
- **Tingkat Kedatangan**: Jumlah pasien yang datang per menit.
- **Total Pasien**: Jumlah keseluruhan pasien yang telah mendapatkan layanan.
- **Waktu Tunggu Rata-rata**: Waktu rata-rata yang dihabiskan pasien dalam antrean sebelum mendapatkan pelayanan medis (dalam menit).
- **Panjang Antrean Rata-rata**: Rata-rata jumlah pasien yang sedang menunggu dalam antrean.
- **Utilisasi Dokter**: Persentase waktu kerja dokter yang digunakan untuk melayani pasien dibandingkan dengan waktu yang tersedia.

## Ringkasan Hasil Simulasi
Simulasi dilakukan dengan variasi jumlah dokter (1 hingga 5 dokter) dan tingkat kedatangan pasien (0.10 hingga 0.30 pasien/menit). Hasil dari simulasi ini dirangkum dalam tabel berikut:

### **1 Dokter**
| Tingkat Kedatangan | Total Pasien | Waktu Tunggu (menit) | Panjang Antrean | Utilisasi (%) |
|------------------|-------------|------------------|----------------|--------------|
| 0.10 | 27.2 | 99.22 | 9.72 | 94.46 |
| 0.15 | 26.6 | 132.70 | 22.37 | 100.24 |
| 0.20 | 28.0 | 171.40 | 32.54 | 103.75 |
| 0.25 | 26.8 | 188.55 | 47.81 | 103.38 |
| 0.30 | 23.4 | 183.38 | 61.05 | 107.37 |

Dapat dilihat bahwa ketika hanya ada satu dokter, waktu tunggu meningkat secara signifikan dengan bertambahnya jumlah pasien.

### **2 Dokter**
| Tingkat Kedatangan | Total Pasien | Waktu Tunggu (menit) | Panjang Antrean | Utilisasi (%) |
|------------------|-------------|------------------|----------------|--------------|
| 0.10 | 42.4 | 41.41 | 5.03 | 86.47 |
| 0.15 | 53.2 | 93.23 | 14.04 | 102.84 |
| 0.20 | 48.6 | 107.35 | 22.28 | 98.38 |
| 0.25 | 50.8 | 127.61 | 37.44 | 102.64 |
| 0.30 | 45.8 | 161.80 | 53.65 | 104.55 |

Dengan dua dokter, antrean sedikit berkurang tetapi masih mengalami overload pada tingkat kedatangan tinggi.

### **3 Dokter**
| Tingkat Kedatangan | Total Pasien | Waktu Tunggu (menit) | Panjang Antrean | Utilisasi (%) |
|------------------|-------------|------------------|----------------|--------------|
| 0.10 | 45.6 | 6.34 | 0.83 | 66.95 |
| 0.15 | 65.6 | 52.51 | 8.66 | 94.41 |
| 0.20 | 67.8 | 84.32 | 18.95 | 100.17 |
| 0.25 | 66.6 | 104.70 | 23.76 | 100.36 |
| 0.30 | 77.6 | 125.42 | 35.25 | 102.20 |

### **4 Dokter**
| Tingkat Kedatangan | Total Pasien | Waktu Tunggu (menit) | Panjang Antrean | Utilisasi (%) |
|------------------|-------------|------------------|----------------|--------------|
| 0.10 | 48.0 | 0.63 | 0.06 | 44.18 |
| 0.15 | 73.4 | 4.64 | 0.75 | 73.64 |
| 0.20 | 86.8 | 14.64 | 2.98 | 89.92 |
| 0.25 | 95.6 | 49.64 | 13.11 | 99.58 |
| 0.30 | 94.6 | 80.98 | 27.00 | 101.94 |

### **5 Dokter**
| Tingkat Kedatangan | Total Pasien | Waktu Tunggu (menit) | Panjang Antrean | Utilisasi (%) |
|------------------|-------------|------------------|----------------|--------------|
| 0.10 | 49.0 | 0.53 | 0.06 | 38.81 |
| 0.15 | 75.4 | 2.91 | 0.48 | 69.11 |
| 0.20 | 95.8 | 4.68 | 0.99 | 80.47 |
| 0.25 | 112.6 | 17.59 | 4.46 | 89.65 |
| 0.30 | 119.2 | 47.30 | 13.48 | 100.30 |

Dapat dilihat jika dokter ditambah hingga lima orang, itu bisa mengurangi antrean secara signifikan.

## Analisis dan Kesimpulan
1. **Tingkat Kedatangan yang Lebih Tinggi Menyebabkan Antrean Lebih Panjang**: Jika jumlah dokter tidak mencukupi untuk menangani pasien yang datang, waktu tunggu meningkat drastis.
2. **Menambah Dokter Mengurangi Waktu Tunggu**: Namun, terlalu banyak dokter tanpa permintaan pasien yang tinggi menyebabkan kurangnya efisiensi pemanfaatan dokter.
3. **Utilisasi Dokter di Atas 100% Menunjukkan Overload**: Jika utilisasi dokter melebihi 100%, artinya kapasitas sistem telah terlampaui, yang dapat menyebabkan penurunan kualitas layanan.
4. **Jumlah Dokter Optimal Tergantung pada Tingkat Kedatangan Pasien**: Untuk setiap tingkat kedatangan, ada jumlah dokter optimal yang meminimalkan antrean dan tetap mempertahankan efisiensi tinggi.


