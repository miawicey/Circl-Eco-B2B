from datetime import datetime


class MaterialLimbah:
    total_material = 0
    SATUAN_STANDAR = "Kg"
    KATEGORI_DEFAULT = "Industri"

    def __init__(self, item_id, kode, nama, jenis_limbah, stok_kg, harga_beli):
        self.item_id = int(item_id)
        self.kode = str(kode)
        self.nama = str(nama)
        self.jenis_limbah = str(jenis_limbah)
        self._stok_kg = float(stok_kg)
        self._harga_beli = float(harga_beli)

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
        return self._harga_beli

    @harga_beli.setter
    def harga_beli(self, value):
        if value < 0:
            raise ValueError("Harga beli material tidak boleh negatif!")
        self._harga_beli = float(value)

    def get_details(self):
        return (
            f"[{self.kode}] {self.nama} ({self.jenis_limbah}) | Stok:"
            f" {self._stok_kg:.1f} {MaterialLimbah.SATUAN_STANDAR} | Harga Beli:"
            f" Rp{self._harga_beli:,.2f}/Kg"
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["item_id"],
            data["kode"],
            data["nama"],
            data["jenis_limbah"],
            data["stok_kg"],
            data["harga_beli"],
        )

    @staticmethod
    def validasi_kode_material(kode):
        return kode.startswith("MAT-") and len(kode) == 7


class ProdukHasilOlahan:
    total_produk = 0
    KATEGORI_UTAMA = "Daur Ulang"
    MINIMAL_STOK_ALERT = 10

    def __init__(self, item_id, kode, nama, stok_unit, harga_jual):
        self.item_id = int(item_id)
        self.kode = str(kode)
        self.nama = str(nama)
        self._stok_unit = int(stok_unit)
        self._harga_jual = float(harga_jual)

        ProdukHasilOlahan.total_produk += 1

    @property
    def stok_unit(self):
        return self._stok_unit

    @stok_unit.setter
    def stok_unit(self, value):
        if value < 0:
            raise ValueError("Stok unit produk tidak boleh negatif!")
        self._stok_unit = int(value)

    @property
    def harga_jual(self):
        return self._harga_jual

    @harga_jual.setter
    def harga_jual(self, value):
        if value < 0:
            raise ValueError("Harga jual produk tidak boleh negatif!")
        self._harga_jual = float(value)

    def get_details(self):
        return (
            f"[{self.kode}] {self.nama} | Stok: {self._stok_unit} Unit | Harga Jual:"
            f" Rp{self._harga_jual:,.2f}/Unit"
        )

    @classmethod
    def set_minimal_stok_alert(cls, batas_baru):
        cls.MINIMAL_STOK_ALERT = int(batas_baru)

    @staticmethod
    def hitung_potensi_pendapatan(stok, harga):
        if stok < 0 or harga < 0:
            return 0.0
        return float(stok * harga)


class TransaksiB2B:
    total_transaksi = 0
    PPN_PERCENT = 0.11
    STATUS_SISTEM = "Aktif"

    def __init__(self, id_trx, nama_klien, produk_obj, jumlah_unit, tgl_transaksi=None):
        self.id_trx = str(id_trx)
        self.produk = produk_obj
        self._nama_klien = str(nama_klien)
        self._jumlah_unit = int(jumlah_unit)
        self._total_bayar = 0.0
        self._tgl_transaksi = (
            tgl_transaksi
            if tgl_transaksi
            else datetime.now().strftime("%Y-%m-%d %H:%M")
        )

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
        return self._total_bayar

    def proses_transaksi(self):
        if self.produk.stok_unit >= self._jumlah_unit:
            self.produk.stok_unit -= self._jumlah_unit
            subtotal = self._jumlah_unit * self.produk.harga_jual
            self._total_bayar = TransaksiB2B.hitung_total_dengan_ppn(subtotal)
            return True, "Transaksi Berhasil Ditransaksikan"
        return False, "Gagal: Stok produk tidak mencukupi"

    def get_details(self):
        return (
            f"[{self._tgl_transaksi}] TRX: {self.id_trx} | Klien: {self._nama_klien}"
            f" | Produk: {self.produk.nama} | Qty: {self._jumlah_unit} Unit | Total"
            f" (inc. PPN): Rp{self._total_bayar:,.2f}"
        )

    @classmethod
    def get_ringkasan_sistem(cls):
        return f"Total Transaksi Terdaftar: {cls.total_transaksi} transaksi."

    @staticmethod
    def hitung_total_dengan_ppn(subtotal):
        return subtotal + (subtotal * TransaksiB2B.PPN_PERCENT)


if __name__ == "__main__":
    mat1 = MaterialLimbah(1, "MAT-001", "Botol Plastik PET", "Biasa", 150.0, 3500)
    mat2 = MaterialLimbah.from_dict({
        "item_id": 2,
        "kode": "MAT-002",
        "nama": "Oli Bekas Industri",
        "jenis_limbah": "B3",
        "stok_kg": 80.0,
        "harga_beli": 8000,
    })

    prd1 = ProdukHasilOlahan(101, "PRD-001", "Paving Block Plastik", 500, 15000)
    prd2 = ProdukHasilOlahan(102, "PRD-002", "Pelumas Daur Ulang", 120, 45000)

    trx1 = TransaksiB2B("TRX-001", "PT Hijau Lestari", prd1, 100)
    trx2 = TransaksiB2B("TRX-002", "CV Mandiri Sejahtera", prd2, 20)

    trx1.proses_transaksi()
    trx2.proses_transaksi()

    print(trx1.get_details())
    print(trx2.get_details())
    print(TransaksiB2B.get_ringkasan_sistem())