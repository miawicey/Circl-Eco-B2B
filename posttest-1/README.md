# Tugas OOP - Sistem Daur Ulang Limbah Industri

Tugas ini dibuat untuk memenuhi tugas praktikum OOP Python, mencakup materi Class & Object, Atribut & Method, serta Encapsulation & Property.
---
## Tema

Sistem sederhana untuk mengelola bisnis daur ulang limbah industri, mulai dari data material limbah masuk, produk hasil olahannya, sampai transaksi penjualan ke klien (B2B).
---
## Isi Program

Ada 3 class yang dibuat:

1. MaterialLimbah
Buat nyimpen data material limbah (bahan baku), kayak jenis limbah, stok, dan harga beli.

2. ProdukHasilOlahan
Buat nyimpen data produk hasil daur ulang yang udah siap dijual, termasuk stok unit dan harga jualnya.

3. TransaksiB2B
Buat nyatet transaksi penjualan produk ke klien. Class ini pake objek dari `ProdukHasilOlahan` di dalamnya, jadi ketiga class ini saling nyambung.
---
## Atribut, Property, Method

- Atribut kelas tiap class punya minimal 3, misalnya `total_material`, `satuan_default`, `ppn`, dll.
- Atribut instance: diisi lewat `__init__`, beda-beda tiap objek.
- Atribut private: pake double underscore (`__harga_beli`, `__harga_jual`, `__total_bayar`) biar beneran ke-protect (name mangling), bukan cuma single underscore yang sebenernya masih bisa diakses bebas.
- Property & setter: dipakai buat akses atribut private tadi, sekalian ada validasi di setter-nya (harga/stok gak boleh negatif, nama klien gak boleh kosong). Kalau input salah, langsung `raise ValueError`.
- Instance method: `get_details()` di tiap class, sama `proses_transaksi()` buat ngurangin stok & hitung total bayar.
- Classmethod: `from_dict()` buat bikin objek dari dictionary, `set_minimal_stok_alert()` buat ubah atribut kelas, `get_ringkasan_sistem()` buat nampilin ringkasan.
- Staticmethod: `validasi_kode_material()`, `hitung_potensi_pendapatan()`, `hitung_total_dengan_ppn()` — fungsi bantu yang gak butuh data dari objek atau class.
---
## Cara Jalanin & OUTPUT sesuai intruksi

python CIRCL-ECO1.py

Detail Material 1: [MAT-001] Botol Plastik PET (Biasa) | Stok: 150.0 Kg | Harga Beli: Rp3500.0/Kg
Detail Material 2: [MAT-002] Oli Bekas Industri (B3) | Stok: 80.0 Kg | Harga Beli: Rp8000.0/Kg
Detail Produk 1: [PRD-001] Paving Block Plastik | Stok: 500 Unit | Harga Jual: Rp15000.0/Unit
Detail Produk 2: [PRD-002] Pelumas Daur Ulang | Stok: 120 Unit | Harga Jual: Rp45000.0/Unit
Detail Transaksi 1: [2026-09-22 18:25] TRX: TRX-001 | Klien: PT Hijau Lestari | Produk: Paving Block Plastik | Qty: 100 Unit | Total (inc. PPN): Rp1665000.0
Detail Transaksi 2: [2026-09-22 18:25] TRX: TRX-002 | Klien: CV Mandiri Sejahtera | Produk: Pelumas Daur Ulang | Qty: 20 Unit | Total (inc. PPN): Rp999000.0
Batas minimal stok produk: 15
Total transaksi terdaftar: 2 transaksi
Cek kode MAT-001 valid? True
Potensi pendapatan produk 1: Rp6000000.0
Subtotal 100rb + PPN jadi: Rp111000.0
Stok material 1 setelah diubah: 200.0 Kg
Harga produk 1 setelah diubah: Rp 17500.0
Nama klien transaksi 1 setelah diubah: PT Hijau Nusantara
Stok negatif ditolak: Stok material tidak boleh negatif!
Harga negatif ditolak: Harga jual tidak boleh negatif!


