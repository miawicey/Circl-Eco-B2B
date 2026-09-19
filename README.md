# CIRCL-ECO: Sistem Waste Management & Circular Economy (Daur Ulang Industri)
CIRCL-ECO adalah program berbasis Object-Oriented Programming (OOP) dalam bahasa Python yang dirancang untuk mengelola ekosistem rantai pasok daur ulang limbah industri. Program ini memodelkan alur pengumpulan bahan baku limbah, pengolahan menjadi produk bernilai tambah, hingga pemrosesan transaksi komersial skala B2B (Business-to-Business).

---

 # Penjelasan Program dan Struktur Class

Program ini dibangun menggunakan 3 class utama yang saling berinteraksi secara independen:

1. Class MaterialLimbah
Class ini berfungsi mengelola data fisik dan finansial dari bahan baku limbah yang dikumpulkan.
 Atribut Kelas: instansi, total_material, SATUAN_STANDAR
  Atribut Instance Public: item_id, kode, nama, jsnis_limbah
 Atribut Instance Private: __stok_kg, __harga_beli
Method:
   Instance method get_details untuk menampilkan rincian data material.
   Class method from_dict sebagai factory method untuk membuat objek dari data dictionary.
  Static method validasi_kode_material untuk memvalidasi format string kode material.
 Property getter dan setter untuk stok_kg dan harga_beli dengan validasi nilai non-negatif.

2. Class ProdukOlahan
Class ini berfungsi mengelola katalog produk hasil proses daur ulang yang siap dijual.
 Atribut Kelas: instansi, total_produk, KATEGORI_UTAMA
 Atribut Instance Public: item_id, kode, nama
  Atribut Instance Private: __stok_unit, __harga_jual
 Method:
   Instance method get_details untuk menampilkan rincian data produk.
    Class method update_instansi untuk memperbarui nama instansi operasional secara global.
   Static method hitung_potensi_pendapatan untuk menghitung estimasi nilai total persediaan.
   Property getter dan setter untuk stok_unit dan harga_jual dengan validasi nilai non-negatif.

3. Class TransaksiB2B
Class ini berfungsi memproses transaksi penjualan B2B dengan menghubungkan data klien dan objek dari ProdukOlahan.
 Atribut Kelas: total_transaksi, PPN_PERCENT
 Atribut Instance Public: id_trx, produk
 Atribut Instance Private: __nama_klien, __jumlah_unit, __total_bayar, __tgl_transaksi
Method:
   Instance method proses_transaksi untuk memotong stok produk secara otomatis dan mengkalkulasi harga akhir.
   Instance method get_details untuk menampilkan rincian data transaksi.
   Class method get_ringkasan_sistem untuk mengambil statistik total transaksi terdaftar.
   Static method hitung_total_dengan_ppn untuk kalkulasi PPN sebesar 11 persen.
   Property getter dan setter untuk nama_klien dengan validasi string tidak boleh kosong, serta getter untuk jumlah_unit dan total_bayar.

---

# Encapsulation dan Validasi Data

Akses terhadap atribut private pada seluruh class dikendalikan menggunakan dekorator property Python.Getter menggunakan dekorator @property untuk membaca nilai atribut private.
 Setter menggunakan dekorator @<nama_properti>.setter untuk mengubah nilai atribut private.
Aturan validasi pada setter:
   Masukan bernilai numerik (stok dan harga) tidak boleh bernilai negatif (< 0).
   Masukan bernilai string (nama klien) tidak boleh kosong atau hanya berisi spasi.
   Jika nilai yang dimasukkan melanggar aturan di atas, setter akan memicu raise ValueError untuk menolak perubahan data.

---

# Panduan Pengujian Program

1. Cara Menjalankan Program
Buka terminal atau lingkungan eksekusi Python, lalu jalankan perintah berikut:
python main.py

2. Alur Pembuktian Pengujian (main.py)
 Pengujian Objek: Program membuat minimal 2 objek untuk setiap class, termasuk pembuatan objek menggunakan class method from_dict.
 Pengujian Method: Program menjalankan seluruh instance method, class method, dan static method untuk memastikan fungsinya berjalan sesuai logika.
 Pengujian Transaksi: Program menjalankan proses transaksi B2B yang secara otomatis mengurangi stok pada objek produk terkait.
  Pengujian Validasi Setter:
   Pengujian Data Valid: Memperbarui nilai stok, harga, dan nama klien dengan data yang benar.
  Pengujian Data Invalid: Memasukkan angka negatif dan string kosong ke dalam setter untuk membuktikan bahwa validasi berhasil menolak data dan ditangkap oleh blok exception handling (try-except).
