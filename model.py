# model.py
import sqlite3

class Mahasiswa:
    """Class Model Mahasiswa menerapkan konsep Encapsulation OOP"""
    def __init__(self, nim, nama, jurusan, ipk):
        self.__nim = nim       # Private attribute (menggunakan __)
        self.__nama = nama
        self.__jurusan = jurusan
        self.__ipk = ipk

    # Getter & Setter
    def get_nim(self): return self.__nim
    def get_nama(self): return self.__nama
    def get_jurusan(self): return self.__jurusan
    def get_ipk(self): return self.__ipk

    def set_nama(self, nama): self.__nama = nama
    def set_jurusan(self, jurusan): self.__jurusan = jurusan
    def set_ipk(self, ipk): self.__ipk = ipk

class DatabaseModel:
    """Class untuk menangani koneksi dan query database SQLite"""
    def __init__(self, db_name="siakad.db"):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        """Menerapkan prinsip DRY untuk koneksi database"""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mahasiswa (
                    nim TEXT PRIMARY KEY,
                    nama TEXT NOT NULL,
                    jurusan TEXT NOT NULL,
                    ipk REAL NOT NULL
                )
            """)
            conn.commit()

    def get_all_mahasiswa(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mahasiswa")
            rows = cursor.fetchall()
            return [Mahasiswa(*row) for row in rows]

    def insert_mahasiswa(self, mhs: Mahasiswa):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mahasiswa VALUES (?, ?, ?, ?)",
                           (mhs.get_nim(), mhs.get_nama(), mhs.get_jurusan(), mhs.get_ipk()))
            conn.commit()

    def update_mahasiswa(self, mhs: Mahasiswa):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE mahasiswa SET nama=?, jurusan=?, ipk=? WHERE nim=?",
                           (mhs.get_nama(), mhs.get_jurusan(), mhs.get_ipk(), mhs.get_nim()))
            conn.commit()

    def delete_mahasiswa(self, nim):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mahasiswa WHERE nim=?", (nim,))
            conn.commit()