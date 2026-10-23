from abc import ABC, abstractmethod
from datetime import datetime


class ItemInventaris(ABC):
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

    @abstractmethod
    def get_details(self):
        pass

    @abstractmethod
    def hitung_nilai_aset(self):
            pass
    def cetak_info(self):
        print(self.get_details())
        print(f"      Nilai aset: Rp{self.hitung_nilai_aset():,.0f}")

    def __str__(self):
        return self.get_details()

    def __eq__(self, other):
        if not isinstance(other, ItemInventaris):
            return NotImplemented
        return self.kode == other.kode

    def __hash__(self):
        return hash(self.kode)

    def __lt__(self, other):
        if not isinstance(other, ItemInventaris):
            return NotImplemented
        return self.hitung_nilai_aset() < other.hitung_nilai_aset()


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
        return (f"[{self.kode}] {self.nama} ({self.jenis_limbah}) | "
                f"Stok: {self._stok} {MaterialLimbah.satuan_default} | "
                f"Harga Beli: Rp{self.__harga_beli:,.0f}/Kg")

    def hitung_nilai_aset(self):
        return self._stok * self.__harga_beli

    @staticmethod
    def validasi_kode_material(kode):
        return kode.startswith("MAT-") and len(kode) == 7


class LimbahB3(MaterialLimbah):

    def __init__(self, item_id, kode, nama, stok_kg, harga_beli, kategori_bahaya="Beracun"):
        super().__init__(item_id, kode, nama, "B3", stok_kg, harga_beli)
        self.kategori_bahaya = str(kategori_bahaya)

    def get_details(self):
        return (super().get_details() +
                f" | PERINGATAN: Limbah B3 ({self.kategori_bahaya})!")


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

    def hitung_nilai_aset(self):
        return self._stok * self.__harga_jual

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