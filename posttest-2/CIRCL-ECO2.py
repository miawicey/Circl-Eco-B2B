from datetime import datetime
 
 
class ItemInventaris:
    total_item = 0
 
    def __init__(self, item_id, kode, nama, stok):
        self.item_id = int(item_id)
        self.kode = str(kode)
        self.nama = str(nama)
        self._stok = float(stok)
        self.__tgl_registrasi = datetime.now().strftime("%Y-%m-%d %H:%M")
        ItemInventaris.total_item += 1
 
    @property
    def stok(self):
        return self._stok
 
    @stok.setter
    def stok(self, value):
        if value < 0:
            raise ValueError("Stok tidak boleh negatif!")
        self._stok = float(value)
 
    def get_tgl_registrasi(self):
        return self.__tgl_registrasi
 
    def get_details(self):
        return f"[{self.kode}] {self.nama} | Stok: {self._stok}"
 
 
class MaterialLimbah(ItemInventaris):
    satuan_default = "Kg"
 
    def __init__(self, item_id, kode, nama, jenis_limbah, stok_kg, harga_beli):
        super().__init__(item_id, kode, nama, stok_kg)
        self.jenis_limbah = str(jenis_limbah)
        self.__harga_beli = float(harga_beli)
 
    @property
    def harga_beli(self):
        return self.__harga_beli
 
    @harga_beli.setter
    def harga_beli(self, value):
        if value < 0:
            raise ValueError("Harga beli tidak boleh negatif!")
        self.__harga_beli = float(value)
 
 
    def get_details(self):
        info = (f"[{self.kode}] {self.nama} ({self.jenis_limbah}) | "
                f"Stok: {self._stok} {MaterialLimbah.satuan_default} | "
                f"Harga Beli: Rp{self.__harga_beli:,.0f}/Kg")
        if self.jenis_limbah.upper() == "B3":
            info += " | PERINGATAN: Limbah B3!"
        return info
 
    @staticmethod
    def validasi_kode_material(kode):
        return kode.startswith("MAT-") and len(kode) == 7
 
 
class ProdukHasilOlahan(ItemInventaris):
    minimal_stok = 10
 
    def __init__(self, item_id, kode, nama, stok_unit, harga_jual, berat_per_unit_kg=1.0):
        super().__init__(item_id, kode, nama, stok_unit)
        self._stok = int(stok_unit)
        self.berat_per_unit_kg = float(berat_per_unit_kg)
        self.__harga_jual = float(harga_jual)
        self.__resep = ResepProduksi(self.kode)
 
    @property
    def stok_unit(self):
        return self._stok
 
    @stok_unit.setter
    def stok_unit(self, value):
        if value < 0:
            raise ValueError("Stok unit tidak boleh negatif!")
        self._stok = int(value)
 
    @property
    def harga_jual(self):
        return self.__harga_jual
 
    @harga_jual.setter
    def harga_jual(self, value):
        if value < 0:
            raise ValueError("Harga jual tidak boleh negatif!")
        self.__harga_jual = float(value)
 
    @property
    def resep(self):
        return self.__resep
 
 
    def get_details(self):
        status = "AMAN" if self._stok >= ProdukHasilOlahan.minimal_stok else "STOK MENIPIS"
        return (f"[{self.kode}] {self.nama} | Stok: {self._stok} Unit ({status}) | "
                f"Harga Jual: Rp{self.__harga_jual:,.0f}/Unit | Berat: {self.berat_per_unit_kg} Kg/Unit")
 
    @classmethod
    def set_minimal_stok_alert(cls, batas_baru):
        cls.minimal_stok = int(batas_baru)
 
 
class ResepProduksi:
    def __init__(self, kode_produk):
        self.kode_produk = kode_produk
        self.__bahan = []
 
    def tambah_bahan(self, nama_material, kg_per_unit):
        self.__bahan.append((nama_material, float(kg_per_unit)))
 
    def get_details(self):
        if not self.__bahan:
            return f"Resep {self.kode_produk}: (belum ada bahan)"
        daftar = ", ".join(f"{n} {kg}Kg" for n, kg in self.__bahan)
        return f"Resep {self.kode_produk}: {daftar}"
 
 
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
 
    def tampilkan_isi(self):
        print(f"    {self.nama_gudang} ({self.lokasi}) - {len(self.__daftar_item)} item")
        for no, item in enumerate(self.__daftar_item, 1):
            print(f"      {no}. {item.get_details()}")
 
 
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
 
    @staticmethod
    def hitung_total_dengan_ppn(subtotal):
        return subtotal + (subtotal * TransaksiB2B.ppn)
 
 
LEBAR = 100
 
 
def judul(teks):
    print()
    print("━" * LEBAR)
    print(f"  {teks}")
    print("━" * LEBAR)
 
 
def sub(teks):
    print(f"\n  ▸ {teks}")
 
 
def uji_setter(objek, atribut, nilai):
    sebelum = getattr(objek, atribut)
    try:
        setattr(objek, atribut, nilai)
        isi = f"{atribut} = {nilai!r}"
        print(f"      ✔  {isi:<36} diterima  ({sebelum!r} → {getattr(objek, atribut)!r})")
    except ValueError as e:
        isi = f"{atribut} = {nilai!r}"
        print(f"      ✘  {isi:<36} ditolak   ({e})")
 
 
if __name__ == "__main__":
    print("╔" + "═" * (LEBAR - 2) + "╗")
    print("║" + "POSTTEST 2 - RELASI UML DAN INHERITANCE".center(LEBAR - 2) + "║")
    print("║" + "Sistem Inventaris Daur Ulang Limbah".center(LEBAR - 2) + "║")
    print("╚" + "═" * (LEBAR - 2) + "╝")
 
    mat1 = MaterialLimbah(1, "MAT-001", "Botol Plastik PET", "Biasa", 150.0, 3500)
    mat2 = MaterialLimbah(2, "MAT-002", "Oli Bekas Industri", "B3", 80.0, 8000)
    prd1 = ProdukHasilOlahan(101, "PRD-001", "Paving Block Plastik", 500, 15000, 2.5)
    prd2 = ProdukHasilOlahan(102, "PRD-002", "Pelumas Daur Ulang", 120, 45000, 1.0)
 
    judul("1. INHERITANCE & METHOD OVERRIDING")
    sub("MaterialLimbah (subclass) - get_details() menambah peringatan B3")
    print("    " + mat1.get_details())
    print("    " + mat2.get_details())
    sub("ProdukHasilOlahan (subclass) - get_details() menambah status stok")
    print("    " + prd1.get_details())
    print("    " + prd2.get_details())
    sub("Atribut private superclass, dibaca lewat method milik superclass")
    print(f"    Tgl registrasi {mat1.kode}: {mat1.get_tgl_registrasi()}")
 
    judul("2. KOMPOSISI  (ProdukHasilOlahan ◆── ResepProduksi)")
    prd1.resep.tambah_bahan(mat1.nama, 2.5)
    prd2.resep.tambah_bahan(mat2.nama, 0.8)
    print("    " + prd1.resep.get_details())
    print("    " + prd2.resep.get_details())
 
    judul("3. AGREGASI  (GudangInventaris ◇── ItemInventaris)")
    gudang = GudangInventaris("Gudang Utama", "Banjarmasin")
    for item in (mat1, mat2, prd1, prd2):
        gudang.tambah_item(item)
    sub("Sebelum item dikeluarkan")
    gudang.tampilkan_isi()
    keluar = gudang.keluarkan_item("MAT-002")
    sub(f"Sesudah {keluar.kode} dikeluarkan (objeknya tetap ada: {keluar.nama})")
    gudang.tampilkan_isi()
 
    judul("4. ASOSIASI  (TransaksiB2B ──> Klien, ProdukHasilOlahan)")
    klien1 = Klien("PT Hijau Lestari", "021-111222")
    klien2 = Klien("CV Mandiri Sejahtera", "0511-333444")
    trx1 = TransaksiB2B("TRX-001", klien1, prd1, 100)
    trx2 = TransaksiB2B("TRX-002", klien2, prd2, 20)
    trx1.proses_transaksi()
    trx2.proses_transaksi()
    print("    " + trx1.get_details())
    print("    " + trx2.get_details())
    print(f"\n    Total transaksi tercatat: {TransaksiB2B.total_transaksi}")
 
    judul("5. VALIDASI SETTER")
    sub("Stok material (MAT-001)")
    uji_setter(mat1, "stok", 200)
    uji_setter(mat1, "stok", -50)
    sub("Harga beli material (MAT-001)")
    uji_setter(mat1, "harga_beli", 4000)
    uji_setter(mat1, "harga_beli", -1)
    sub("Stok produk (PRD-001)")
    uji_setter(prd1, "stok_unit", 300)
    uji_setter(prd1, "stok_unit", -5)
    sub("Harga jual produk (PRD-001)")
    uji_setter(prd1, "harga_jual", 17500)
    uji_setter(prd1, "harga_jual", -10000)
    sub("Nama klien")
    uji_setter(klien1, "nama", "PT Hijau Nusantara")
    uji_setter(klien1, "nama", "   ")
    print()
 
