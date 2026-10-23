## Sistem Inventaris & Transaksi B2B Daur Ulang Limbah
Aplikasi CLI berbasis Python yang menerapkan konsep Object-Oriented Programming (OOP) untuk mengelola inventaris gudang daur ulang limbah dan transaksi B2B (termasuk perhitungan PPN 11%). Program ini dibangun menggunakan pustaka standar Python (standard library).
---
## File & Cara Menjalankan
1. inventaris.py — Struktur kelas item inventaris dan resep.
2. main.py — Logika gudang, data klien, transaksi B2B, dan menu interaktif.
Jalankan program melalui terminal:
Bash
python main.py
Saran: Pilih Menu 11 (Muat Data Contoh) saat pertama kali menjalankan program untuk mengisi data awal secara otomatis

## 1. Relasi UML
1. Asosiasi (TransaksiB2B → Klien & ProdukHasilOlahan)
Objek Klien dan Produk dikirim lewat constructor TransaksiB2B. Kedua objek ini dibuat terpisah di luar transaksi, sehingga kehancuran objek transaksi tidak memengaruhi data klien maupun produk.

2. Agregasi (GudangInventaris ◇— ItemInventaris)
Gudang menampung daftar item. Item dibuat terpisah di luar gudang sebelum dimasukkan, dan jika item dikeluarkan dari gudang, objeknya tetap ada di memori.

3. Komposisi (ProdukHasilOlahan ◆— ResepProduksi)
Objek ResepProduksi diinstansiasi secara internal di dalam constructor produk (self.__resep). Resep tidak bisa berdiri sendiri tanpa adanya produk dan akan ikut terhapus jika objek produk dihapus.

## 2. Abstraksi, Polimorfisme, & SOLID
a. Abstraksi
Abstract Base Class: ItemInventaris(ABC) menjadi cetak biru utama.

1.  Abstract Method: get_details() dan hitung_nilai_aset() wajib diimplementasikan oleh subclass (MaterialLimbah dan ProdukHasilOlahan).

2. Shared Method: cetak_info() langsung digunakan oleh semua subclass tanpa perlu di-override.

3. Proteksi Kelas Abstrak: Menu 10 (uji_abstract) membuktikan bahwa ItemInventaris menolak pembuatan objek langsung dengan memicu TypeError.

b. Polimorfisme
Pewarisan (Override): MaterialLimbah, LimbahB3, dan ProdukHasilOlahan mengimputasi perilaku get_details() dan hitung_nilai_aset() masing-masing.

1. Duck Typing: GudangInventaris dan TransaksiB2B bukan dari hirarki yang sama, tetapi keduanya punya fungsi ringkasan() sehingga sama-sama bisa diproses oleh fungsi cetak_ringkasan(objek).

2. Operator Overloading:
ItemInventaris: __str__, __eq__ (pembandingan kode), __lt__ (pengurutan nilai aset via sorted()), __hash__.
GudangInventaris: __len__, __iter__.
TransaksiB2B: __str__, __add__, __radd__ (penjumlahan total transaksi dengan operator +).

c. Prinsip SOLID
Open/Closed Principle (OCP): Penambahan variasi baru seperti LimbahB3 dilakukan lewat subclass tanpa mengubah logika pada MaterialLimbah atau GudangInventaris.
Liskov Substitution Principle (LSP): Seluruh subclass dari ItemInventaris dapat dipakai bergantian dalam list gudang tanpa merusak alur program.
Dependency Inversion Principle (DIP): TransaksiB2B memanfaatkan dependency injection dengan menerima objek klien dan produk dari luar.

## 3. Tangkapan Layar Output
a. Uji Abstract Class (Menu 10)
b. Polimorfisme via Pewarisan (Menu 4)
c. Duck Typing & Operator Overloading (Menu 8 & 9)
d. DICOBA SEMUAAA YA BANGG mau saya lanjut ke web nantinya hehehehe :3