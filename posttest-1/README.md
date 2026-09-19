Program terdiri dari 3 class utama

1. MaterialLimbah
   - *Deskripsi:* Mengelola data bahan baku limbah industri.
   - *Atribut Kelas:* total_material, SATUAN_STANDAR ("Kg"), KATEGORI_DEFAULT ("Industri").
   - *Atribut Instance Public:* item_id, kode, nama, jenis_limbah.
   - *Atribut Instance Protected:* _stok_kg, _harga_beli.

2. ProdukHasilOlahan
   - *Deskripsi:* Mengelola katalog produk daur ulang yang siap dijual.
   - *Atribut Kelas:* total_produk, KATEGORI_UTAMA ("Daur Ulang"), MINIMAL_STOK_ALERT (10).
   - *Atribut Instance Public:* item_id, kode, nama.
   - *Atribut Instance Protected:* _stok_unit, _harga_jual.

3. TransaksiB2B
   - *Deskripsi:* Memproses transaksi penjualan B2B dengan menghubungkan langsung ke objek ProdukHasilOlahan.
   - *Atribut Kelas:* total_transaksi, PPN_PERCENT (0.11), STATUS_SISTEM ("Aktif").
   - *Atribut Instance Public:* id_trx, produk.
   - *Atribut Instance Protected:* _nama_klien, _jumlah_unit, _total_bayar, _tgl_transaksi.

---

# 2. Penerapan Jenis Method

Setiap class mengimplementasikan tiga jenis method wajib dalam OOP:

- *Instance Method:*
  - MaterialLimbah.get_details() : Menampilkan detail spesifikasi material.
  - ProdukHasilOlahan.get_details() : Menampilkan detail katalog produk.
  - TransaksiB2B.proses_transaksi() : Memotong stok produk otomatis dan mengkalkulasi total tagihan.
  - TransaksiB2B.get_details() : Menampilkan rincian transaksi B2B terproses.

- *Class Method (@classmethod):*
  - MaterialLimbah.from_dict() : Membuat objek baru langsung dari data berformat dictionary.
  - ProdukHasilOlahan.set_minimal_stok_alert() : Mengubah ambang batas stok minimal alert secara global.
  - TransaksiB2B.get_ringkasan_sistem() : Mengambil status ringkasan total transaksi terdaftar.

- *Static Method (@staticmethod):*
  - MaterialLimbah.validasi_kode_material() : Memvalidasi format prefix kode material (harus diawali MAT- dan 7 karakter).
  - ProdukHasilOlahan.hitung_potensi_pendapatan() : Menghitung estimasi total nilai persediaan produk.
  - TransaksiB2B.hitung_total_dengan_ppn() : Mengkalkulasi nilai total pembayaran beserta PPN 11 persen.

---

# 3. Encapsulation & Validasi Setter (@property)

Atribut terlindungi (_stok_kg, _harga_beli, _stok_unit, _harga_jual, _nama_klien) dikontrol ketat menggunakan dekorator @property dan @<nama_properti>.setter:

- *Getter (@property):* Memberikan akses baca terhadap nilai atribut protected.
- *Setter (@<nama_properti>.setter):* Memvalidasi nilai input sebelum diperbarui:
  - Nilai numerik (stok dan harga) ditolak jika kurang dari nol (< 0) dengan melempar ValueError.
  - Nama klien pada transaksi ditolak jika berupa string kosong atau spasi dengan melempar ValueError.

---

# 4. Simulasi Eksekusi (circl-eco1.py)

Saat file main.py dijalankan, program secara otomatis:
1. Menginisialisasi objek material (termasuk menggunakan @classmethod from_dict).
2. Menginisialisasi objek produk hasil olahan.
3. Membuat dan memproses objek transaksi B2B (trx1 dan trx2).
4. Mengubah stok produk terkait secara otomatis setelah transaksi sukses. test
