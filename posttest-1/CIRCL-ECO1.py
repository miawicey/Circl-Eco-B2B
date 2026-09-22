from datetime import datetime

class MaterialLimbah:
    total_material = 0
    satuan_default = "Kg"
    kategori_default = "Industri"

    def __init__(self, item_id, kode, nama, jenis_limbah, stok_kg, harga_beli):
        self.item_id = int(item_id)
        self.kode = str(kode)
        self.nama = str(nama)
        self.jenis_limbah = str(jenis_limbah)
        self._stok_kg = float(stok_kg)
        self.__harga_beli = float(harga_beli)
        MaterialLimbah.total_material += 1

    @property
    def stok_kg(self):
        return self._stok_kg

    @stok_kg.setter
    def stok_kg(self, value):
        if value < 0:
            raise ValueError("Stok material tidak boleh negatif!")
        self._stok_kg = float(value)

    @property
    def harga_beli(self):
        return self.__harga_beli

    @harga_beli.setter
    def harga_beli(self, value):
        if value < 0:
            raise ValueError("Harga beli tidak boleh negatif!")
        self.__harga_beli = float(value)

    def get_details(self):
        return f"[{self.kode}] {self.nama} ({self.jenis_limbah}) | Stok: {self._stok_kg} {MaterialLimbah.satuan_default} | Harga Beli: Rp{self.__harga_beli}/Kg"

    @classmethod
    def from_dict(cls, data):
        return cls(data["item_id"], data["kode"], data["nama"], data["jenis_limbah"], data["stok_kg"], data["harga_beli"])

    @staticmethod
    def validasi_kode_material(kode):
        return kode.startswith("MAT-") and len(kode) == 7


class ProdukHasilOlahan:
    total_produk = 0
    kategori = "Daur Ulang"
    minimal_stok = 10

    def __init__(self, item_id, kode, nama, stok_unit, harga_jual):
        self.item_id = int(item_id)
        self.kode = str(kode)
        self.nama = str(nama)
        self._stok_unit = int(stok_unit)
        self.__harga_jual = float(harga_jual)
        ProdukHasilOlahan.total_produk += 1

    @property
    def stok_unit(self):
        return self._stok_unit

    @stok_unit.setter
    def stok_unit(self, value):
        if value < 0:
            raise ValueError("Stok unit tidak boleh negatif!")
        self._stok_unit = int(value)

    @property
    def harga_jual(self):
        return self.__harga_jual

    @harga_jual.setter
    def harga_jual(self, value):
        if value < 0:
            raise ValueError("Harga jual tidak boleh negatif!")
        self.__harga_jual = float(value)

    def get_details(self):
        return f"[{self.kode}] {self.nama} | Stok: {self._stok_unit} Unit | Harga Jual: Rp{self.__harga_jual}/Unit"

    @classmethod
    def set_minimal_stok_alert(cls, batas_baru):
        cls.minimal_stok = int(batas_baru)

    @staticmethod
    def hitung_potensi_pendapatan(stok, harga):
        if stok < 0 or harga < 0:
            return 0.0
        return float(stok * harga)


class TransaksiB2B:
    total_transaksi = 0
    ppn = 0.11
    status = "Aktif"

    def __init__(self, id_trx, nama_klien, produk_obj, jumlah_unit, tgl_transaksi=None):
        self.id_trx = str(id_trx)
        self.produk = produk_obj
        self._nama_klien = str(nama_klien)
        self._jumlah_unit = int(jumlah_unit)
        self.__total_bayar = 0.0
        self._tgl_transaksi = tgl_transaksi if tgl_transaksi else datetime.now().strftime("%Y-%m-%d %H:%M")
        TransaksiB2B.total_transaksi += 1

    @property
    def nama_klien(self):
        return self._nama_klien

    @nama_klien.setter
    def nama_klien(self, value):
        if not value or not str(value).strip():
            raise ValueError("Nama klien tidak boleh kosong!")
        self._nama_klien = str(value).strip()

    @property
    def jumlah_unit(self):
        return self._jumlah_unit

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
        return f"[{self._tgl_transaksi}] TRX: {self.id_trx} | Klien: {self._nama_klien} | Produk: {self.produk.nama} | Qty: {self._jumlah_unit} Unit | Total (inc. PPN): Rp{self.__total_bayar}"

    @classmethod
    def get_ringkasan_sistem(cls):
        return f"Total transaksi terdaftar: {cls.total_transaksi} transaksi"

    @staticmethod
    def hitung_total_dengan_ppn(subtotal):
        return subtotal + (subtotal * TransaksiB2B.ppn)


if __name__ == "__main__":
    mat1 = MaterialLimbah(1, "MAT-001", "Botol Plastik PET", "Biasa", 150.0, 3500)
    mat2 = MaterialLimbah.from_dict({
        "item_id": 2, "kode": "MAT-002", "nama": "Oli Bekas Industri",
        "jenis_limbah": "B3", "stok_kg": 80.0, "harga_beli": 8000
    })

    prd1 = ProdukHasilOlahan(101, "PRD-001", "Paving Block Plastik", 500, 15000)
    prd2 = ProdukHasilOlahan(102, "PRD-002", "Pelumas Daur Ulang", 120, 45000)

    trx1 = TransaksiB2B("TRX-001", "PT Hijau Lestari", prd1, 100)
    trx2 = TransaksiB2B("TRX-002", "CV Mandiri Sejahtera", prd2, 20)

    print("Detail Material 1:", mat1.get_details())
    print("Detail Material 2:", mat2.get_details())
    print("Detail Produk 1:", prd1.get_details())
    print("Detail Produk 2:", prd2.get_details())

    trx1.proses_transaksi()
    trx2.proses_transaksi()
    print("Detail Transaksi 1:", trx1.get_details())
    print("Detail Transaksi 2:", trx2.get_details())

    ProdukHasilOlahan.set_minimal_stok_alert(15)
    print("Batas minimal stok produk:", ProdukHasilOlahan.minimal_stok)
    print(TransaksiB2B.get_ringkasan_sistem())
    print("Cek kode MAT-001 valid?", MaterialLimbah.validasi_kode_material("MAT-001"))

    potensi = ProdukHasilOlahan.hitung_potensi_pendapatan(prd1.stok_unit, prd1.harga_jual)
    print(f"Potensi pendapatan produk 1: Rp{potensi}")
    print("Subtotal 100rb + PPN jadi:", f"Rp{TransaksiB2B.hitung_total_dengan_ppn(100000)}")

    mat1.stok_kg = 200.0
    prd1.harga_jual = 17500.0
    trx1.nama_klien = "PT Hijau Nusantara"
    print("Stok material 1 setelah diubah:", mat1.stok_kg, "Kg")
    print("Harga produk 1 setelah diubah: Rp", prd1.harga_jual)
    print("Nama klien transaksi 1 setelah diubah:", trx1.nama_klien)

    # coba isi data yang salah, harusnya ditolak sama setter
    try:
        mat1.stok_kg = -50.0
    except ValueError as e:
        print("Stok negatif ditolak:", e)

    try:
        prd1.harga_jual = -10000.0
    except ValueError as e:
        print("Harga negatif ditolak:", e)

    try:
        trx1.nama_klien = "   "
    except ValueError as e:
        print("Nama klien kosong ditolak:", e)