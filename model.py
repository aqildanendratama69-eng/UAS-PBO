import sqlite3
from abc import ABC, abstractmethod  # [Pertemuan 9: Abstraksi]

# ==========================================
# [Pertemuan 9: Abstraksi]
# Membuat Abstract Base Class (ABC) sebagai kerangka dasar
# ==========================================
class Person(ABC):
    def __init__(self, nama):
        self.nama = nama
        
    @abstractmethod
    def get_role(self):
        """Metode abstrak yang wajib diimplementasikan oleh subclass"""
        pass

# ==========================================
# [Pertemuan 2: Konsep Class, Objek, dan Atribut]
# [Pertemuan 6: Pewarisan Sifat (Inheritance)] -> Mahasiswa mewarisi Person
# ==========================================
class Mahasiswa(Person):
    """Class Model Mahasiswa menerapkan konsep Encapsulation OOP"""
    
    # [Pertemuan 3: Method & Parameter Self]
    def __init__(self, nim, nama, jurusan, tahun):
        super().__init__(nama) # Memanggil constructor parent class
        
        # [Pertemuan 4: Encapsulation]
        # Menggunakan double underscore (__) untuk private attributes
        self.__nim = nim       
        self.__jurusan = jurusan
        self.__tahun = tahun

    # [Pertemuan 4: Encapsulation] - Getter & Setter
    def get_nim(self): return self.__nim
    def get_nama(self): return self.nama
    def get_jurusan(self): return self.__jurusan
    def get_tahun(self): return self.__tahun

    def set_nama(self, nama): self.nama = nama
    def set_jurusan(self, jurusan): self.__jurusan = jurusan
    def set_tahun(self, tahun): self.__tahun = tahun

    # ==========================================
    # [Pertemuan 6: Method Overriding] & [Pertemuan 7: Polymorphism]
    # Meng-override metode abstrak dari class Person
    # ==========================================
    def get_role(self):
        return "Mahasiswa Aktif"

# ==========================================
# [Pertemuan 11: Integrasi OOP dan Basis Data Relasional (CRUD dengan SQLite)]
# ==========================================
class DatabaseModel:
    """Class untuk menangani koneksi dan query database SQLite"""
    def __init__(self, db_name="siakad.db"):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mahasiswa (
                    nim TEXT PRIMARY KEY,
                    nama TEXT NOT NULL,
                    jurusan TEXT NOT NULL,
                    tahun TEXT
                )
            """)
            conn.commit()

    def get_all_mahasiswa(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mahasiswa")
            rows = cursor.fetchall()
            return [Mahasiswa(row[0], row[1], row[2], row[3]) for row in rows]

    def insert_mahasiswa(self, mhs: Mahasiswa):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mahasiswa VALUES (?, ?, ?, ?)",
                           (mhs.get_nim(), mhs.get_nama(), mhs.get_jurusan(), mhs.get_tahun()))
            conn.commit()

    def update_mahasiswa(self, mhs: Mahasiswa):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE mahasiswa SET nama=?, jurusan=?, tahun=? WHERE nim=?",
                           (mhs.get_nama(), mhs.get_jurusan(), mhs.get_tahun(), mhs.get_nim()))
            conn.commit()

    def delete_mahasiswa(self, nim):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mahasiswa WHERE nim=?", (nim,))
            conn.commit()

    def search_mahasiswa(self, keyword):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM mahasiswa WHERE nim LIKE ? OR nama LIKE ? OR jurusan LIKE ?",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
            )
            rows = cursor.fetchall()
            return [Mahasiswa(row[0], row[1], row[2], row[3]) for row in rows]