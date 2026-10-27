from inventaris import (ItemInventaris, MaterialLimbah, LimbahB3,
                        ProdukHasilOlahan)


class GudangInventaris:
    def __init__(self, nama_gudang, lokasi):
        self.nama_gudang = nama_gudang
        self.lokasi = lokasi
        self.__daftar_item = []

    def tambah_item(self, item):
        self.__daftar_item.append(item)

    def keluarkan_item(self, kode):
        for item in self.__daftar_item:
            if item.kode == kode:
                self.__daftar_item.remove(item)
                return item
        return None

    def cari_item(self, kode):
        for item in self.__daftar_item:
            if item.kode == kode:
                return item
        return None

    def total_nilai_aset(self):
        return sum(item.hitung_nilai_aset() for item in self.__daftar_item)

    def tampilkan_isi(self):
        print(f"Gudang {self.nama_gudang} ({self.lokasi}) - {len(self)} item:")
        for item in self.__daftar_item:
            print("  -", item.get_details())

    # Duck typing: punya ringkasan(), tanpa pewarisan dengan TransaksiB2B
    def ringkasan(self):
        return (f"Gudang {self.nama_gudang}: {len(self)} item, "
                f"total aset Rp{self.total_nilai_aset():,.0f}")

    # Operator overloading
    def __len__(self):
        return len(self.__daftar_item)

    def __iter__(self):
        return iter(self.__daftar_item)


class Klien:
    def __init__(self, nama, kontak):
        self._nama = ""
        self.nama = nama
        self.kontak = kontak

    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, value):
        if not value or not str(value).strip():
            raise ValueError("Nama klien tidak boleh kosong!")
        self._nama = str(value).strip()


class TransaksiB2B:
    ppn = 0.11
    total_transaksi = 0

    def __init__(self, id_trx, klien_obj, produk_obj, jumlah_unit):
        self.id_trx = str(id_trx)
        self.klien = klien_obj
        self.produk = produk_obj
        self._jumlah_unit = int(jumlah_unit)
        self.__total_bayar = 0.0
        TransaksiB2B.total_transaksi += 1

    @property
    def total_bayar(self):
        return self.__total_bayar

    def proses_transaksi(self):
        if self.produk.stok_unit >= self._jumlah_unit:
            self.produk.stok_unit -= self._jumlah_unit
            subtotal = self._jumlah_unit * self.produk.harga_jual
            self.__total_bayar = TransaksiB2B.hitung_total_dengan_ppn(subtotal)
            return True, "Transaksi berhasil"
        return False, "Gagal, stok produk tidak cukup"

    def get_details(self):
        return (f"TRX: {self.id_trx} | Klien: {self.klien.nama} | Produk: {self.produk.nama} | "
                f"Qty: {self._jumlah_unit} Unit | Total (inc. PPN): Rp{self.__total_bayar:,.0f}")

    def ringkasan(self):
        return (f"{self.id_trx}: {self.klien.nama} membeli {self._jumlah_unit} "
                f"{self.produk.nama}, total Rp{self.__total_bayar:,.0f}")

    def __str__(self):
        return self.get_details()

    def __add__(self, other):
        nilai = other if isinstance(other, (int, float)) else other.total_bayar
        return self.__total_bayar + nilai

    __radd__ = __add__   
    @staticmethod
    def hitung_total_dengan_ppn(subtotal):
        return subtotal + (subtotal * TransaksiB2B.ppn)


def cetak_ringkasan(objek):
    print("  *", objek.ringkasan())


def judul(teks):
    print()
    print(teks.upper())
    print("-" * len(teks))


def baca_teks(prompt):
    while True:
        nilai = input(prompt).strip()
        if nilai:
            return nilai
        print("  Input tidak boleh kosong.")


def baca_angka(prompt, tipe=float):
    while True:
        try:
            nilai = tipe(input(prompt).strip().replace(",", "."))
            if nilai < 0:
                print("  Nilai tidak boleh negatif.")
                continue
            return nilai
        except ValueError:
            print("  Masukkan angka yang valid.")


def baca_pilihan(prompt, valid):
    while True:
        nilai = input(prompt).strip().lower()
        if nilai in valid:
            return nilai
        print(f"  Pilihan harus salah satu dari: {', '.join(valid)}")


def pilih_dari(daftar, label, tampil):
    if not daftar:
        print(f"  Belum ada {label}.")
        return None
    for no, obj in enumerate(daftar, 1):
        print(f"  {no}. {tampil(obj)}")
    no = baca_angka(f"Pilih {label} (nomor): ", int)
    if 1 <= no <= len(daftar):
        return daftar[no - 1]
    print("  Nomor tidak ada dalam daftar.")
    return None

class Aplikasi:
    def __init__(self):
        self.gudang = GudangInventaris("Gudang Utama", "Banjarmasin")
        self.daftar_material = []
        self.daftar_produk = []
        self.daftar_klien = []
        self.daftar_transaksi = []
        self.menu = [
            ("Tambah material limbah", self.tambah_material),
            ("Tambah produk hasil olahan", self.tambah_produk),
            ("Tambah bahan ke resep produk", self.tambah_resep),
            ("Lihat isi gudang", self.lihat_gudang),
            ("Keluarkan item dari gudang", self.keluarkan_item),
            ("Tambah klien", self.tambah_klien),
            ("Buat transaksi B2B", self.buat_transaksi),
            ("Ringkasan gudang dan transaksi", self.lihat_ringkasan),
            ("Bandingkan dan urutkan item", self.bandingkan_item),
            ("Uji abstract class", self.uji_abstract),
            ("Muat data contoh", self.muat_contoh),
        ]

    def _id_berikut(self):
        return ItemInventaris.total_item + 1

    def _kode_tersedia(self, kode):
        if self.gudang.cari_item(kode):
            print("  Kode sudah dipakai item lain.")
            return False
        return True

    def tambah_material(self):
        judul("Tambah material limbah")
        kode = baca_teks("Kode (format MAT-XXX): ").upper()
        if not MaterialLimbah.validasi_kode_material(kode):
            print("  Format kode tidak valid. Contoh: MAT-001")
            return
        if not self._kode_tersedia(kode):
            return
        nama = baca_teks("Nama material: ")
        stok = baca_angka("Stok (Kg): ")
        harga = baca_angka("Harga beli per Kg (Rp): ")
        if baca_pilihan("Termasuk limbah B3? (y/n): ", ["y", "n"]) == "y":
            kategori = baca_teks("Kategori bahaya (mis. Beracun): ")
            item = LimbahB3(self._id_berikut(), kode, nama, stok, harga, kategori)
        else:
            jenis = baca_teks("Jenis limbah (mis. Plastik): ")
            item = MaterialLimbah(self._id_berikut(), kode, nama, jenis, stok, harga)
        self.gudang.tambah_item(item)
        self.daftar_material.append(item)
        print("  Berhasil ditambahkan ke gudang:")
        print("  ", item)

    def tambah_produk(self):
        judul("Tambah produk hasil olahan")
        kode = baca_teks("Kode (format PRD-XXX): ").upper()
        if not kode.startswith("PRD-"):
            print("  Format kode tidak valid. Contoh: PRD-001")
            return
        if not self._kode_tersedia(kode):
            return
        nama = baca_teks("Nama produk: ")
        stok = baca_angka("Stok (unit): ", int)
        harga = baca_angka("Harga jual per unit (Rp): ")
        berat = baca_angka("Berat per unit (Kg): ")
        item = ProdukHasilOlahan(self._id_berikut(), kode, nama, stok, harga, berat)
        self.gudang.tambah_item(item)
        self.daftar_produk.append(item)
        print("  Berhasil ditambahkan ke gudang:")
        print("  ", item)

    def tambah_resep(self):
        judul("Tambah bahan ke resep produk")
        produk = pilih_dari(self.daftar_produk, "produk", lambda p: f"{p.kode} {p.nama}")
        if produk is None:
            return
        material = pilih_dari(self.daftar_material, "material", lambda m: f"{m.kode} {m.nama}")
        if material is None:
            return
        kg = baca_angka("Kebutuhan material per unit produk (Kg): ")
        produk.resep.tambah_bahan(material.nama, kg)
        print("  ", produk.resep.get_details())

    def tambah_klien(self):
        judul("Tambah klien")
        nama = input("Nama klien: ")
        kontak = baca_teks("Kontak: ")
        try:
            klien = Klien(nama, kontak)
        except ValueError as e:
            print("  Ditolak:", e)
            return
        self.daftar_klien.append(klien)
        print(f"  Klien {klien.nama} berhasil ditambahkan.")

    def lihat_gudang(self):
        judul(f"Isi {self.gudang.nama_gudang} ({self.gudang.lokasi})")
        if len(self.gudang) == 0:
            print("  Gudang masih kosong.")
            return
        for no, item in enumerate(self.gudang, 1):
            print(f"{no}. ", end="")
            item.cetak_info()
        print(f"\nTotal item  : {len(self.gudang)}")
        print(f"Total aset  : Rp{self.gudang.total_nilai_aset():,.0f}")
        for produk in self.daftar_produk:
            print(" ", produk.resep.get_details())

    def keluarkan_item(self):
        judul("Keluarkan item dari gudang")
        if len(self.gudang) == 0:
            print("  Gudang masih kosong.")
            return
        for item in self.gudang:
            print(f"  {item.kode}  {item.nama}")
        kode = baca_teks("Kode item yang dikeluarkan: ").upper()
        item = self.gudang.keluarkan_item(kode)
        if item is None:
            print("  Kode tidak ditemukan di gudang.")
            return
        for daftar in (self.daftar_material, self.daftar_produk):
            if item in daftar:
                daftar.remove(item)
        print(f"  {item.nama} dikeluarkan. Objeknya tetap ada, hanya tidak lagi di gudang (agregasi).")

    def buat_transaksi(self):
        judul("Buat transaksi B2B")
        klien = pilih_dari(self.daftar_klien, "klien", lambda k: f"{k.nama} ({k.kontak})")
        if klien is None:
            return
        produk = pilih_dari(self.daftar_produk, "produk",
                            lambda p: f"{p.kode} {p.nama} | stok {p.stok_unit} | Rp{p.harga_jual:,.0f}")
        if produk is None:
            return
        jumlah = baca_angka("Jumlah unit: ", int)
        id_trx = f"TRX-{len(self.daftar_transaksi) + 1:03d}"
        trx = TransaksiB2B(id_trx, klien, produk, jumlah)
        berhasil, pesan = trx.proses_transaksi()
        print(" ", pesan)
        if berhasil:
            self.daftar_transaksi.append(trx)
            print("  ", trx)

    def lihat_ringkasan(self):
        judul("Ringkasan")
        # Duck typing: satu fungsi untuk dua kelas yang tidak berhubungan
        cetak_ringkasan(self.gudang)
        for trx in self.daftar_transaksi:
            cetak_ringkasan(trx)
        if self.daftar_transaksi:
            print(f"\nTotal pendapatan (operator +): Rp{sum(self.daftar_transaksi):,.0f}")

    def bandingkan_item(self):
        judul("Bandingkan dan urutkan item")
        items = list(self.gudang)
        if len(items) < 2:
            print("  Minimal 2 item di gudang.")
            return
        a = pilih_dari(items, "item pertama", lambda i: f"{i.kode} {i.nama}")
        b = pilih_dari(items, "item kedua", lambda i: f"{i.kode} {i.nama}")
        if a is None or b is None:
            return
        print(f"\n  {a.kode} == {b.kode}  ->  {a == b}")
        print(f"  {a.kode} <  {b.kode}  ->  {a < b}  (nilai aset {a.hitung_nilai_aset():,.0f} vs {b.hitung_nilai_aset():,.0f})")
        print("\nUrutan nilai aset dari terkecil:")
        for item in sorted(items):
            print(f"  {item.kode}  Rp{item.hitung_nilai_aset():,.0f}")

    def uji_abstract(self):
        judul("Uji abstract class")
        try:
            ItemInventaris(0, "XXX-000", "Item Abstrak", 1)
        except TypeError as e:
            print("  TypeError:", e)

    def muat_contoh(self):
        judul("Muat data contoh")
        mat1 = MaterialLimbah(self._id_berikut(), "MAT-001", "Botol Plastik PET", "Plastik", 150, 3500)
        mat2 = LimbahB3(self._id_berikut() + 1, "MAT-002", "Oli Bekas Industri", 80, 8000, "Mudah Terbakar")
        prd1 = ProdukHasilOlahan(self._id_berikut() + 2, "PRD-001", "Paving Block Plastik", 500, 15000, 2.5)
        prd2 = ProdukHasilOlahan(self._id_berikut() + 3, "PRD-002", "Pelumas Daur Ulang", 120, 45000, 1.0)
        for item in (mat1, mat2, prd1, prd2):
            if not self.gudang.cari_item(item.kode):
                self.gudang.tambah_item(item)
        self.daftar_material += [m for m in (mat1, mat2) if m not in self.daftar_material]
        self.daftar_produk += [p for p in (prd1, prd2) if p not in self.daftar_produk]
        prd1.resep.tambah_bahan(mat1.nama, 2.5)
        prd2.resep.tambah_bahan(mat2.nama, 0.8)
        self.daftar_klien += [Klien("PT Hijau Lestari", "021-111222"),
                              Klien("CV Mandiri Sejahtera", "0511-333444")]
        print("  2 material, 2 produk, dan 2 klien dimuat.")

    def jalankan(self):
        print("SISTEM INVENTARIS DAN TRANSAKSI B2B DAUR ULANG LIMBAH")
        aksi = {str(no): fungsi for no, (_, fungsi) in enumerate(self.menu, 1)}
        while True:
            judul("Menu utama")
            for no, (nama, _) in enumerate(self.menu, 1):
                print(f"  {no:>2}. {nama}")
            print("   0. Keluar")
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "0":
                print("\nTerima kasih.")
                break
            if pilihan in aksi:
                aksi[pilihan]()
            else:
                print("  Menu tidak tersedia.")


if __name__ == "__main__":
    try:
        Aplikasi().jalankan()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram dihentikan.")