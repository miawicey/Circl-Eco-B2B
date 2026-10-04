## Posttest 2 - Relasi UML dan Inheritance


Program Python sederhana untuk mengelola inventaris daur ulang limbah: material limbah, produk hasil olahan, gudang, klien, dan transaksi penjualan.
---
## Cara Menjalankan
1. python posttest_simple.py


# Kelas yang Ada
1. ItemInventaris: superclass untuk semua barang inventaris.
2. MaterialLimbah: subclass dari ItemInventaris, untuk bahan baku berupa limbah.
3. ProdukHasilOlahan: subclass dari ItemInventaris, untuk produk jadi hasil daur ulang.
4. ResepProduksi: daftar bahan yang dipakai sebuah produk.
5. GudangInventaris: tempat menyimpan kumpulan item.
6. Klien: data pelanggan.
7. Invoice: rincian tagihan (subtotal, PPN, total) milik sebuah transaksi.
8. TransaksiB2B: transaksi penjualan produk ke klien, lengkap dengan PPN 11%.


# Relasi UML
1. Asosiasi: TransaksiB2B berhubungan dengan Klien dan ProdukHasilOlahan. Keduanya dibuat di luar transaksi.
2. Agregasi: GudangInventaris berisi ItemInventaris. Item dibuat di luar gudang dan tetap ada walaupun dikeluarkan dari gudang.
3. Komposisi :
a. ProdukHasilOlahan membuat ResepProduksi sendiri di dalam konstruktornya. Resep disimpan private dan hanya diakses lewat method produk (tambah_bahan() dan get_resep()), jadi resep tidak berdiri sendiri tanpa produknya.
b. TransaksiB2B membuat Invoice sendiri di dalam konstruktornya. Invoice disimpan private dan dihitung saat transaksi diproses, jadi tidak ada invoice tanpa transaksi.
4. Inheritance
Superclass: ItemInventaris.
Subclass: MaterialLimbah dan ProdukHasilOlahan. Keduanya memanggil super().__init__(...).


# Atribut tambahan:
1. MaterialLimbah: jenis_limbah dan harga_beli.
2. ProdukHasilOlahan: berat_per_unit_kg dan harga_jual.
3. Method overriding: get_details() dari ItemInventaris ditulis ulang di kedua subclass. MaterialLimbah menambahkan peringatan untuk limbah B3, sedangkan ProdukHasilOlahan menampilkan status stok (AMAN atau STOK MENIPIS) dan berat per unit.
3. Protected: _stok di ItemInventaris, dipakai langsung oleh kedua subclass.
4. Private: __tgl_registrasi di ItemInventaris, hanya bisa dibaca lewat get_tgl_registrasi().

--- 
# Validasi

Setter berikut menolak nilai tidak valid dengan ValueError:
1. stok (tidak boleh negatif)
2. harga_beli (tidak boleh negatif)
3. stok_unit (tidak boleh negatif)
4. harga_jual (tidak boleh negatif)
5. nama pada Klien (tidak boleh kosong)

# OUTPUT

[MAT-001] Botol Plastik PET (Biasa) | Stok: 150.0 Kg | Harga Beli: Rp3,500/Kg
[MAT-002] Oli Bekas Industri (B3) | Stok: 80.0 Kg | Harga Beli: Rp8,000/Kg | PERINGATAN: Limbah B3!
[PRD-001] Paving Block Plastik | Stok: 500 Unit (AMAN) | Harga Jual: Rp15,000/Unit | Berat: 2.5 Kg/Unit
[PRD-002] Pelumas Daur Ulang | Stok: 120 Unit (AMAN) | Harga Jual: Rp45,000/Unit | Berat: 1.0 Kg/Unit
Tgl registrasi: 2026-10-04 22:07

Resep PRD-001: Botol Plastik PET 2.5Kg
Resep PRD-002: Oli Bekas Industri 0.8Kg

Gudang Gudang Utama (Banjarmasin) - 4 item:
  - [MAT-001] Botol Plastik PET (Biasa) | Stok: 150.0 Kg | Harga Beli: Rp3,500/Kg
  - [MAT-002] Oli Bekas Industri (B3) | Stok: 80.0 Kg | Harga Beli: Rp8,000/Kg | PERINGATAN: Limbah B3!
  - [PRD-001] Paving Block Plastik | Stok: 500 Unit (AMAN) | Harga Jual: Rp15,000/Unit | Berat: 2.5 Kg/Unit
  - [PRD-002] Pelumas Daur Ulang | Stok: 120 Unit (AMAN) | Harga Jual: Rp45,000/Unit | Berat: 1.0 Kg/Unit
Item dikeluarkan: Oli Bekas Industri
Gudang Gudang Utama (Banjarmasin) - 3 item:
  - [MAT-001] Botol Plastik PET (Biasa) | Stok: 150.0 Kg | Harga Beli: Rp3,500/Kg
  - [PRD-001] Paving Block Plastik | Stok: 500 Unit (AMAN) | Harga Jual: Rp15,000/Unit | Berat: 2.5 Kg/Unit
  - [PRD-002] Pelumas Daur Ulang | Stok: 120 Unit (AMAN) | Harga Jual: Rp45,000/Unit | Berat: 1.0 Kg/Unit

TRX: TRX-001 | Klien: PT Hijau Lestari | Produk: Paving Block Plastik | Qty: 100 Unit | Total (inc. PPN): Rp1,665,000 | Invoice: INV-TRX-001
TRX: TRX-002 | Klien: CV Mandiri Sejahtera | Produk: Pelumas Daur Ulang | Qty: 20 Unit | Total (inc. PPN): Rp999,000 | Invoice: INV-TRX-002
Total transaksi: 2

Stok negatif ditolak: Stok tidak boleh negatif!
Harga beli negatif ditolak: Harga beli tidak boleh negatif!
Stok unit negatif ditolak: Stok unit tidak boleh negatif!
Harga negatif ditolak: Harga jual tidak boleh negatif!
Nama klien kosong ditolak: Nama klien tidak boleh kosong!