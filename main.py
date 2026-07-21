import tkinter as tk
from tkinter import messagebox
import sqlite3
from model import DatabaseModel, Mahasiswa
from view import MainView

# ==========================================
# [Pertemuan 5: Relasi Antar Objek]
# Controller memiliki relasi 'Association/Composition' dengan Model dan View
# ==========================================
class Controller:
    """Controller menghubungkan Model dan View (MVC Pattern)"""
    def __init__(self, model: DatabaseModel, view: MainView):
        self.model = model
        self.view = view
        self.form_view = self.view.form_frame

        self.bind_events()
        self.load_data()

    # ==========================================
    # [Pertemuan 13: Event Handling GUI & Integrasi Database]
    # ==========================================
    def bind_events(self):
        """Menghubungkan tombol di View dengan fungsi logic di Controller"""
        self.form_view.btn_simpan.config(command=self.create_data)
        self.form_view.btn_update.config(command=self.update_data)
        self.form_view.btn_hapus.config(command=self.delete_data)
        self.form_view.btn_clear.config(command=self.form_view.clear_form)
        self.form_view.btn_cari.config(command=self.search_data)
        self.form_view.btn_tampil_semua.config(command=self.load_data)
        
        # Event khusus untuk double click pada tabel Treeview
        self.form_view.tree.bind("<Double-1>", self.on_tree_select)
        
        # Event khusus untuk menekan tombol Enter pada keyboard saat pencarian
        self.form_view.ent_search.bind("<Return>", lambda e: self.search_data())

    def load_data(self):
        """Read: Memperbarui Treeview dari Database"""
        for item in self.form_view.tree.get_children():
            self.form_view.tree.delete(item)

        try:
            mahasiswa_list = self.model.get_all_mahasiswa()
            # Loop data dari model dan masukkan ke tabel di view
            for mhs in mahasiswa_list:
                self.form_view.tree.insert("", tk.END, values=(
                    mhs.get_nim(), mhs.get_nama(), mhs.get_jurusan(), mhs.get_tahun()
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data database: {e}")

    def search_data(self):
        """Cari data mahasiswa berdasarkan keyword"""
        keyword = self.form_view.get_search_keyword()
        if not keyword:
            messagebox.showwarning("Peringatan", "Masukkan kata kunci pencarian!")
            return

        for item in self.form_view.tree.get_children():
            self.form_view.tree.delete(item)

        try:
            results = self.model.search_mahasiswa(keyword)
            if results:
                for mhs in results:
                    self.form_view.tree.insert("", tk.END, values=(
                        mhs.get_nim(), mhs.get_nama(), mhs.get_jurusan(), mhs.get_tahun()
                    ))
            else:
                messagebox.showinfo("Info", f"Data dengan kata kunci '{keyword}' tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mencari data: {e}")

    def validate_input(self, nim, nama, jurusan, tahun):
        """Validasi input form"""
        if not all([nim, nama, jurusan]):
            raise ValueError("NIM, Nama, dan Jurusan wajib diisi!")
        return tahun if tahun else None

    # ==========================================
    # [Pertemuan 10: Exception Handling & Persistensi Data]
    # Menggunakan blok try-except-finally untuk menangkap error validasi/database
    # ==========================================
    def create_data(self):
        """Create Data ke Database"""
        nim, nama, jurusan, tahun = self.form_view.get_form_data()
        try:
            self.validate_input(nim, nama, jurusan, tahun)
            mhs = Mahasiswa(nim, nama, jurusan, tahun)
            self.model.insert_mahasiswa(mhs)
            
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil didaftarkan!")
            self.form_view.clear_form()
            self.load_data()
        except sqlite3.IntegrityError:
            # Menangkap error spesifik bawaan SQLite jika Primary Key kembar
            messagebox.showerror("Gagal", f"NIM {nim} sudah terdaftar di sistem!")
        except ValueError as ve:
            # Menangkap error validasi form kosong
            messagebox.showwarning("Peringatan", str(ve))
        except Exception as e:
            # Menangkap error umum lainnya
            messagebox.showerror("Error Terjadi", f"Kesalahan sistem: {e}")
        finally:
            pass # Blok ini selalu dieksekusi meskipun terjadi error

    def update_data(self):
        """Update Data dengan Kunci Primary Key"""
        nim, nama, jurusan, tahun = self.form_view.get_form_data()
        try:
            if self.form_view.ent_nim["state"] != "readonly":
                raise ValueError("Silakan pilih data dari tabel dengan klik ganda terlebih dahulu sebelum update!")
            self.validate_input(nim, nama, jurusan, tahun)
            mhs = Mahasiswa(nim, nama, jurusan, tahun)
            self.model.update_mahasiswa(mhs)
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil diperbarui!")
            self.form_view.clear_form()
            self.load_data()
        except ValueError as ve:
            messagebox.showwarning("Peringatan", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def delete_data(self):
        """Delete Data dengan Dialog Konfirmasi"""
        selected = self.form_view.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data pada tabel yang ingin dihapus!")
            return

        nim = self.form_view.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus data dengan NIM {nim}?"):
            try:
                self.model.delete_mahasiswa(nim)
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.form_view.clear_form()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def on_tree_select(self, event):
        """Memuat data dari Treeview ke form dan mengunci Primary Key"""
        selected = self.form_view.tree.selection()
        if selected:
            data = self.form_view.tree.item(selected[0])['values']
            self.form_view.load_to_form(data[0], data[1], data[2], data[3])

if __name__ == "__main__":
    db = DatabaseModel()
    app = MainView()
    controller = Controller(db, app)
    app.mainloop()