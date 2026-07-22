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

class MataKuliah:
    """Model untuk data Mata Kuliah"""
    def __init__(self, kode_mk, nama_mk, sks):
        self.kode_mk = kode_mk
        self.nama_mk = nama_mk
        self.sks = sks

class KRSItem:
    """Model untuk satu item mata kuliah di KRS Mahasiswa"""
    def __init__(self, id_krs, nim, kode_mk, nama_mk, sks):
        self.id_krs = id_krs
        self.nim = nim
        self.kode_mk = kode_mk
        self.nama_mk = nama_mk
        self.sks = sks

# ==========================================
# [Pertemuan 11: Integrasi OOP dan Basis Data Relasional (CRUD dengan SQLite)]
# ==========================================
class DatabaseModel:
    """Class untuk menangani koneksi dan query database SQLite"""
    def __init__(self, db_name="siakad.db"):
        self.db_name = db_name
        self.create_table()
        self.insert_mata_kuliah_default() # Isi otomatis data matkul

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Tabel Mahasiswa
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mahasiswa (
                    nim TEXT PRIMARY KEY,
                    nama TEXT NOT NULL,
                    jurusan TEXT NOT NULL,
                    tahun TEXT
                )
            """)
            # Tabel Mata Kuliah
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mata_kuliah (
                    kode_mk TEXT PRIMARY KEY,
                    nama_mk TEXT NOT NULL,
                    sks INTEGER NOT NULL
                )
            """)
            # Tabel KRS (Relasi Many-to-Many antara Mahasiswa dan Mata Kuliah)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS krs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nim TEXT NOT NULL,
                    kode_mk TEXT NOT NULL,
                    FOREIGN KEY(nim) REFERENCES mahasiswa(nim) ON DELETE CASCADE,
                    FOREIGN KEY(kode_mk) REFERENCES mata_kuliah(kode_mk) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def insert_mata_kuliah_default(self):
        """Memasukkan data default mata kuliah agar tabel tidak kosong"""
        matkul_default = [
            ("MK001", "Pemrograman Berorientasi Objek", 3),
            ("MK002", "Basis Data", 3),
            ("MK003", "Struktur Data", 3),
            ("MK004", "Algoritma Pemrograman", 4),
            ("MK005", "Jaringan Komputer", 3),
            ("MK006", "Sistem Operasi", 3),
            ("MK007", "Kecerdasan Buatan", 3),
            ("MK008", "Matematika Diskrit", 2),
        ]
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for mk in matkul_default:
                cursor.execute("INSERT OR IGNORE INTO mata_kuliah VALUES (?, ?, ?)", mk)
            conn.commit()

    # ==========================================
    # FUNGSI CRUD MAHASISWA
    # ==========================================
    def get_all_mahasiswa(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mahasiswa")
            rows = cursor.fetchall()
            return [Mahasiswa(row[0], row[1], row[2], row[3]) for row in rows]

    def get_mahasiswa_by_nim(self, nim):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mahasiswa WHERE nim=?", (nim,))
            row = cursor.fetchone()
            if row:
                return Mahasiswa(row[0], row[1], row[2], row[3])
            return None

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
            # Aktifkan pragma foreign_keys agar data krs yang berelasi ikut terhapus
            cursor.execute("PRAGMA foreign_keys = ON")
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

    # ==========================================
    # FUNGSI KRS & MATA KULIAH
    # ==========================================
    def get_all_mata_kuliah(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mata_kuliah")
            rows = cursor.fetchall()
            return [MataKuliah(*row) for row in rows]

    def get_krs_by_nim(self, nim):
        """Mengambil data KRS yang direlasikan dengan tabel mata kuliah"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT k.id, k.nim, m.kode_mk, m.nama_mk, m.sks 
                FROM krs k
                JOIN mata_kuliah m ON k.kode_mk = m.kode_mk
                WHERE k.nim = ?
            """, (nim,))
            rows = cursor.fetchall()
            return [KRSItem(*row) for row in rows]

    def add_krs_item(self, nim, kode_mk):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Cek duplikasi agar tidak mengambil matkul yang sama dua kali
            cursor.execute("SELECT id FROM krs WHERE nim=? AND kode_mk=?", (nim, kode_mk))
            if cursor.fetchone():
                raise sqlite3.IntegrityError("Mata kuliah sudah diambil!")
                
            cursor.execute("INSERT INTO krs (nim, kode_mk) VALUES (?, ?)", (nim, kode_mk))
            conn.commit()

    def delete_krs_item(self, id_krs):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM krs WHERE id=?", (id_krs,))
            conn.commit()