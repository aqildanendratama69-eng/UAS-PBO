# main.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from model import DatabaseModel, Mahasiswa
from view import MainView

class Controller:
    def __init__(self, model: DatabaseModel, view: MainView):
        self.model = model
        self.view = view
        self.form_view = self.view.frames["FormMahasiswaFrame"]
        
        self.bind_events()
        self.load_data()
        self.view.show_frame("DashboardFrame") # Tampilkan dashboard pertama kali

    def bind_events(self):
        self.form_view.btn_simpan.config(command=self.create_data)
        self.form_view.btn_update.config(command=self.update_data)
        self.form_view.btn_hapus.config(command=self.delete_data)
        self.form_view.btn_clear.config(command=self.form_view.clear_form)
        self.form_view.tree.bind("<Double-1>", self.on_tree_select)

    def load_data(self):
        """Read: Memperbarui Treeview dari Database"""
        for item in self.form_view.tree.get_children():
            self.form_view.tree.delete(item)
        
        try:
            mahasiswa_list = self.model.get_all_mahasiswa()
            for mhs in mahasiswa_list:
                self.form_view.tree.insert("", tk.END, values=(
                    mhs.get_nim(), mhs.get_nama(), mhs.get_jurusan(), mhs.get_ipk()
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data database: {e}")

    def validate_input(self, nim, nama, jurusan, ipk_str):
        if not all([nim, nama, jurusan, ipk_str]):
            raise ValueError("Semua kolom wajib diisi!")
        try:
            ipk = float(ipk_str)
            if ipk < 0.0 or ipk > 4.0:
                raise ValueError("IPK harus berada di rentang 0.00 - 4.00")
            return ipk
        except ValueError as e:
            if "could not convert" in str(e):
                raise ValueError("Kolom IPK wajib berupa angka/desimal (titik)!")
            raise e

    def create_data(self):
        """Create Data dengan Try-Except-Finally"""
        nim, nama, jurusan, ipk_str = self.form_view.get_form_data()
        try:
            ipk = self.validate_input(nim, nama, jurusan, ipk_str)
            mhs = Mahasiswa(nim, nama, jurusan, ipk)
            self.model.insert_mahasiswa(mhs)
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil disimpan!")
            self.form_view.clear_form()
            self.load_data()
        except sqlite3.IntegrityError:
            messagebox.showerror("Gagal", f"NIM {nim} sudah terdaftar di sistem!")
        except ValueError as ve:
            messagebox.showwarning("Peringatan", str(ve))
        except Exception as e:
            messagebox.showerror("Error Terjadi", f"Kesalahan sistem: {e}")
        finally:
            pass # Pastikan memori/resources siap untuk aksi berikutnya

    def update_data(self):
        """Update Data dengan Kunci Primary Key[cite: 1]"""
        nim, nama, jurusan, ipk_str = self.form_view.get_form_data()
        try:
            if self.form_view.ent_nim["state"] != "readonly":
                raise ValueError("Silakan pilih data dari tabel dengan klik ganda terlebih dahulu sebelum update!")
            ipk = self.validate_input(nim, nama, jurusan, ipk_str)
            mhs = Mahasiswa(nim, nama, jurusan, ipk)
            self.model.update_mahasiswa(mhs)
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil diperbarui[cite: 1]!")
            self.form_view.clear_form()
            self.load_data()
        except ValueError as ve:
            messagebox.showwarning("Peringatan", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def delete_data(self):
        """Delete Data dengan Dialog Konfirmasi[cite: 1]"""
        selected = self.form_view.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data pada tabel yang ingin dihapus!")
            return
        
        nim = self.form_view.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus data dengan NIM {nim}?"):
            try:
                self.model.delete_mahasiswa(nim)
                messagebox.showinfo("Sukses", "Data berhasil dihapus[cite: 1]!")
                self.form_view.clear_form()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def on_tree_select(self, event):
        """Memuat data dari Treeview ke form dan mengunci Primary Key[cite: 1]"""
        selected = self.form_view.tree.selection()
        if selected:
            data = self.form_view.tree.item(selected[0])['values']
            self.form_view.load_to_form(data[0], data[1], data[2], data[3])

if __name__ == "__main__":
    db = DatabaseModel()
    app = MainView()
    controller = Controller(db, app)
    app.mainloop()