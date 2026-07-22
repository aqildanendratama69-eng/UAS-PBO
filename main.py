import tkinter as tk
from tkinter import messagebox
import sqlite3
from model import DatabaseModel, Mahasiswa
from view import MainView

class Controller:
    def __init__(self, model: DatabaseModel, view: MainView):
        self.model = model
        self.view = view
        
        self.login_view = self.view.frames["LoginFrame"]
        self.dashboard_view = self.view.frames["DashboardFrame"]
        self.form_view = self.view.frames["FormMahasiswaFrame"]
        self.krs_view = self.view.frames["FormKRSFrame"] # Bind frame KRS
        
        self.view.trigger_logout = self.logout

        self.bind_events()
        self.load_data()
        self.load_mata_kuliah() # Muat tabel kiri KRS
        
        self.view.show_menu(False)
        self.view.show_frame("LoginFrame")

    def bind_events(self):
        # Event Login
        self.login_view.btn_login.config(command=self.proses_login)
        self.login_view.ent_password.bind("<Return>", lambda e: self.proses_login())

        # Event Halaman Mahasiswa
        self.form_view.btn_simpan.config(command=self.create_data)
        self.form_view.btn_update.config(command=self.update_data)
        self.form_view.btn_hapus.config(command=self.delete_data)
        self.form_view.btn_clear.config(command=self.form_view.clear_form)
        self.form_view.btn_cari.config(command=self.search_data)
        self.form_view.btn_tampil_semua.config(command=self.load_data)
        self.form_view.tree.bind("<Double-1>", self.on_tree_select)
        self.form_view.ent_search.bind("<Return>", lambda e: self.search_data())

        # Event Halaman KRS
        self.krs_view.btn_cek_mhs.config(command=self.cek_mahasiswa_krs)
        self.krs_view.ent_nim_krs.bind("<Return>", lambda e: self.cek_mahasiswa_krs())
        self.krs_view.tree_mk.bind("<Double-1>", self.tambah_krs) # Klik ganda untuk tambah ke KRS
        self.krs_view.btn_hapus_krs.config(command=self.hapus_krs)
        
        # Event CRUD Mata Kuliah
        self.krs_view.btn_tambah_mk.config(command=self.tambah_mk)
        self.krs_view.btn_update_mk.config(command=self.update_mk)
        self.krs_view.btn_hapus_mk.config(command=self.hapus_mk)
        self.krs_view.btn_clear_mk.config(command=self.krs_view.clear_mk_form)
        self.krs_view.tree_mk.bind("<<TreeviewSelect>>", self.on_tree_mk_select)

    # ==========================================
    # LOGIKA HALAMAN MAHASISWA (CRUD)
    # ==========================================
    def load_data(self):
        for item in self.form_view.tree.get_children():
            self.form_view.tree.delete(item)
        try:
            mahasiswa_list = self.model.get_all_mahasiswa()
            for index, mhs in enumerate(mahasiswa_list):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.form_view.tree.insert("", tk.END, values=(
                    mhs.get_nim(), mhs.get_nama(), mhs.get_jurusan(), mhs.get_tahun()
                ), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data database: {e}")

    def search_data(self):
        keyword = self.form_view.get_search_keyword()
        if not keyword:
            messagebox.showwarning("Peringatan", "Masukkan kata kunci pencarian!")
            return
        for item in self.form_view.tree.get_children():
            self.form_view.tree.delete(item)
        try:
            results = self.model.search_mahasiswa(keyword)
            if results:
                for index, mhs in enumerate(results):
                    tag = "evenrow" if index % 2 == 0 else "oddrow"
                    self.form_view.tree.insert("", tk.END, values=(mhs.get_nim(), mhs.get_nama(), mhs.get_jurusan(), mhs.get_tahun()), tags=(tag,))
            else:
                messagebox.showinfo("Info", f"Data dengan kata kunci '{keyword}' tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mencari data: {e}")

    def validate_input(self, nim, nama, jurusan, tahun):
        if not all([nim, nama, jurusan]):
            raise ValueError("NIM, Nama, dan Jurusan wajib diisi!")
        return tahun if tahun else None

    def create_data(self):
        nim, nama, jurusan, tahun = self.form_view.get_form_data()
        try:
            self.validate_input(nim, nama, jurusan, tahun)
            mhs = Mahasiswa(nim, nama, jurusan, tahun)
            self.model.insert_mahasiswa(mhs)
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil didaftarkan!")
            self.form_view.clear_form()
            self.load_data()
        except sqlite3.IntegrityError:
            messagebox.showerror("Gagal", f"NIM {nim} sudah terdaftar di sistem!")
        except ValueError as ve:
            messagebox.showwarning("Peringatan", str(ve))
        except Exception as e:
            messagebox.showerror("Error Terjadi", f"Kesalahan sistem: {e}")
        finally:
            pass

    def update_data(self):
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
            
            # Jika mahasiswa yang diupdate sedang dibuka di form KRS, refresh namanya
            nim_krs_aktif = self.krs_view.ent_nim_krs.get().strip()
            if nim_krs_aktif == nim:
                self.cek_mahasiswa_krs()

        except ValueError as ve:
            messagebox.showwarning("Peringatan", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")
        finally:
            pass

    def delete_data(self):
        selected = self.form_view.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data pada tabel yang ingin dihapus!")
            return
        nim = self.form_view.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus data dengan NIM {nim}? (KRS terkait juga akan terhapus)"):
            try:
                self.model.delete_mahasiswa(nim)
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.form_view.clear_form()
                self.load_data()
                
                # Bersihkan tampilan form KRS jika NIM yang dihapus sedang dibuka
                if self.krs_view.ent_nim_krs.get().strip() == nim:
                    self.krs_view.ent_nim_krs.delete(0, tk.END)
                    self.krs_view.lbl_info_mhs.config(text="Pilih mahasiswa untuk mulai mengisi KRS.")
                    self.krs_view.lbl_sks.config(text="Total SKS: 0")
                    for item in self.krs_view.tree_krs.get_children():
                        self.krs_view.tree_krs.delete(item)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")
            finally:
                pass

    def on_tree_select(self, event):
        selected = self.form_view.tree.selection()
        if selected:
            data = self.form_view.tree.item(selected[0])['values']
            self.form_view.load_to_form(data[0], data[1], data[2], data[3])

    # ==========================================
    # LOGIKA HALAMAN KRS
    # ==========================================
    def load_mata_kuliah(self):
        """Memuat daftar semua mata kuliah ke tabel kiri Form KRS"""
        for item in self.krs_view.tree_mk.get_children():
            self.krs_view.tree_mk.delete(item)
        
        matkul_list = self.model.get_all_mata_kuliah()
        for index, mk in enumerate(matkul_list):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.krs_view.tree_mk.insert("", tk.END, values=(mk.kode_mk, mk.nama_mk, mk.sks), tags=(tag,))

    def cek_mahasiswa_krs(self):
        """Mengecek apakah NIM valid, jika valid muat data KRS-nya"""
        nim = self.krs_view.ent_nim_krs.get().strip()
        if not nim:
            messagebox.showwarning("Peringatan", "Masukkan NIM terlebih dahulu!")
            return
            
        mhs = self.model.get_mahasiswa_by_nim(nim)
        if not mhs:
            messagebox.showerror("Gagal", f"Mahasiswa dengan NIM {nim} tidak ditemukan di database.")
            self.krs_view.lbl_info_mhs.config(text="Mahasiswa tidak ditemukan.")
            self.krs_view.lbl_sks.config(text="Total SKS: 0")
            for item in self.krs_view.tree_krs.get_children():
                self.krs_view.tree_krs.delete(item)
            return
            
        self.krs_view.lbl_info_mhs.config(text=f"Aktif: {mhs.get_nama()} ({mhs.get_jurusan()})")
        self.load_krs_mahasiswa(nim)

    def load_krs_mahasiswa(self, nim):
        """Memuat daftar KRS mahasiswa ke tabel kanan dan menghitung SKS"""
        for item in self.krs_view.tree_krs.get_children():
            self.krs_view.tree_krs.delete(item)
            
        krs_list = self.model.get_krs_by_nim(nim)
        total_sks = 0
        
        for index, krs in enumerate(krs_list):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.krs_view.tree_krs.insert("", tk.END, values=(krs.id_krs, krs.kode_mk, krs.nama_mk, krs.sks), tags=(tag,))
            total_sks += krs.sks
            
        self.krs_view.lbl_sks.config(text=f"Total SKS: {total_sks}")

    def tambah_krs(self, event):
        """Menambahkan MK dari tabel kiri ke tabel KRS Kanan (Double-click event)"""
        nim = self.krs_view.ent_nim_krs.get().strip()
        if not nim or "Aktif:" not in self.krs_view.lbl_info_mhs.cget("text"):
            messagebox.showwarning("Peringatan", "Cari dan aktifkan Mahasiswa terlebih dahulu sebelum mengisi KRS!")
            return
            
        selected = self.krs_view.tree_mk.selection()
        if not selected: return
        
        mk_kode = self.krs_view.tree_mk.item(selected[0])['values'][0]
        mk_nama = self.krs_view.tree_mk.item(selected[0])['values'][1]
        
        try:
            self.model.add_krs_item(nim, mk_kode)
            self.load_krs_mahasiswa(nim) # Refresh tabel KRS kanan
        except sqlite3.IntegrityError:
            messagebox.showinfo("Info", f"Mata kuliah '{mk_nama}' sudah ada di KRS!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan KRS: {e}")

    def hapus_krs(self):
        """Menghapus MK dari KRS (Tombol Hapus)"""
        nim = self.krs_view.ent_nim_krs.get().strip()
        if not nim: return
        
        selected = self.krs_view.tree_krs.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih mata kuliah di tabel KRS (kanan) yang ingin dihapus!")
            return
            
        krs_id = self.krs_view.tree_krs.item(selected[0])['values'][0]
        mk_nama = self.krs_view.tree_krs.item(selected[0])['values'][2]
        
        if messagebox.askyesno("Konfirmasi Batal KRS", f"Yakin ingin membatalkan mata kuliah '{mk_nama}'?"):
            try:
                self.model.delete_krs_item(krs_id)
                self.load_krs_mahasiswa(nim) # Refresh
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus KRS: {e}")

    # ==========================================
    # LOGIKA CRUD MATA KULIAH (Form Kiri)
    # ==========================================
    def on_tree_mk_select(self, event):
        selected = self.krs_view.tree_mk.selection()
        if selected:
            data = self.krs_view.tree_mk.item(selected[0])['values']
            self.krs_view.load_to_mk_form(data[0], data[1], data[2])

    def tambah_mk(self):
        kode, nama, sks = self.krs_view.get_mk_data()
        if not all([kode, nama, sks]):
            messagebox.showwarning("Peringatan", "Kode, Nama MK, dan SKS wajib diisi!")
            return
        try:
            from model import MataKuliah
            mk = MataKuliah(kode, nama, int(sks))
            self.model.insert_mata_kuliah(mk)
            self.load_mata_kuliah()
            self.krs_view.clear_mk_form()
            messagebox.showinfo("Sukses", "Mata kuliah baru berhasil ditambahkan!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Gagal", f"Mata kuliah dengan kode {kode} sudah ada!")
        except ValueError:
            messagebox.showwarning("Peringatan", "SKS harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah MK: {e}")

    def update_mk(self):
        kode, nama, sks = self.krs_view.get_mk_data()
        if not all([kode, nama, sks]):
            messagebox.showwarning("Peringatan", "Pilih mata kuliah lalu isi datanya dengan lengkap!")
            return
        if self.krs_view.ent_kode_mk["state"] != "readonly":
            messagebox.showwarning("Peringatan", "Pilih mata kuliah dari tabel terlebih dahulu!")
            return
        try:
            from model import MataKuliah
            mk = MataKuliah(kode, nama, int(sks))
            self.model.update_mata_kuliah(mk)
            self.load_mata_kuliah()
            self.krs_view.clear_mk_form()
            # Refresh tabel KRS jika matkul yg diupdate ada di KRS
            nim = self.krs_view.ent_nim_krs.get().strip()
            if nim and "Aktif:" in self.krs_view.lbl_info_mhs.cget("text"):
                self.load_krs_mahasiswa(nim)
            messagebox.showinfo("Sukses", "Mata kuliah berhasil diperbarui!")
        except ValueError:
            messagebox.showwarning("Peringatan", "SKS harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengupdate MK: {e}")

    def hapus_mk(self):
        selected = self.krs_view.tree_mk.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih mata kuliah yang ingin dihapus dari tabel!")
            return
        kode = self.krs_view.tree_mk.item(selected[0])['values'][0]
        nama = self.krs_view.tree_mk.item(selected[0])['values'][1]
        if messagebox.askyesno("Konfirmasi Hapus", f"Yakin ingin menghapus mata kuliah '{nama}'?\n\nPERINGATAN: Mahasiswa yang sudah mengambil matkul ini di KRS-nya juga akan kehilangan data KRS tersebut!"):
            try:
                self.model.delete_mata_kuliah(kode)
                self.load_mata_kuliah()
                self.krs_view.clear_mk_form()
                # Refresh tabel KRS
                nim = self.krs_view.ent_nim_krs.get().strip()
                if nim and "Aktif:" in self.krs_view.lbl_info_mhs.cget("text"):
                    self.load_krs_mahasiswa(nim)
                messagebox.showinfo("Sukses", "Mata kuliah berhasil dihapus!")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus MK: {e}")

    # ==========================================
    # LOGIKA AUTHENTIKASI & APLIKASI
    # ==========================================
    def proses_login(self):
        username = self.login_view.ent_username.get().strip()
        password = self.login_view.ent_password.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password harus diisi!")
            return
            
        is_valid, role = self.model.verify_login(username, password)
        if is_valid:
            # Update statistik dashboard sebelum menampilkannya
            total_mhs, total_mk, total_krs = self.model.get_dashboard_stats()
            self.dashboard_view.update_stats(role, total_mhs, total_mk, total_krs)
            
            messagebox.showinfo("Sukses", f"Selamat datang, {role}!")
            self.login_view.ent_username.delete(0, tk.END)
            self.login_view.ent_password.delete(0, tk.END)
            self.view.show_menu(True)
            self.view.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Gagal", "Username atau Password salah!")

    def logout(self):
        if messagebox.askyesno("Logout", "Apakah Anda yakin ingin keluar?"):
            self.view.show_menu(False)
            self.view.show_frame("LoginFrame")

if __name__ == "__main__":
    db = DatabaseModel()
    app = MainView()
    controller = Controller(db, app)
    app.mainloop()