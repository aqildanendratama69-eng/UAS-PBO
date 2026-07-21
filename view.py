import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# [Pertemuan 12: Pengantar GUI Python (Tkinter): Window, Widget & Layout]
# ==========================================

# ==========================================
# [Pertemuan 6: Pewarisan Sifat (Inheritance)]
# Class DashboardFrame mewarisi properti dari tk.Frame
# ==========================================
class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg="#f4f6f9")
        
        label_judul = tk.Label(self, text="Sistem Manajemen Mahasiswa (SIAKAD)", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#333")
        label_judul.pack(pady=40)
        
        label_sub = tk.Label(self, text="Selamat Datang di Aplikasi Manajemen Data Mahasiswa\nGunakan Menu Bar di atas untuk menavigasi aplikasi.", font=("Arial", 12), bg="#f4f6f9", justify="center")
        label_sub.pack(pady=10)

# ==========================================
# [Pertemuan 6: Pewarisan Sifat (Inheritance)]
# Class FormMahasiswaFrame mewarisi properti dari tk.Frame
# ==========================================
class FormMahasiswaFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg="#f0f0f0")
        self.setup_ui()

    def setup_ui(self):
        # [Pertemuan 12: Layout Management (pack, grid)]
        # ==================== JUDUL ====================
        label_judul = tk.Label(
            self,
            text="Form Manajemen Mahasiswa",
            font=("Times New Roman", 18, "bold"),
            bg="#f0f0f0",
            fg="#8B0000"  # Dark red / maroon
        )
        label_judul.pack(pady=(20, 15))

        # ==================== KOTAK PENCARIAN ====================
        frame_search = tk.Frame(self, bg="#f0f0f0")
        frame_search.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(frame_search, text="Kotak Pencarian:", font=("Arial", 10), bg="#f0f0f0").pack(side="left", padx=(0, 5))

        self.ent_search = tk.Entry(frame_search, width=35, font=("Arial", 10))
        self.ent_search.pack(side="left", padx=(0, 10))

        self.btn_cari = tk.Button(
            frame_search, text="Cari Data", bg="#003366", fg="white",
            font=("Arial", 9, "bold"), width=12, cursor="hand2"
        )
        self.btn_cari.pack(side="left", padx=5)

        self.btn_tampil_semua = tk.Button(
            frame_search, text="Tampilkan Semua", bg="#555555", fg="white",
            font=("Arial", 9, "bold"), width=14, cursor="hand2"
        )
        self.btn_tampil_semua.pack(side="left", padx=5)

        # ==================== FORM DATA MAHASISWA ====================
        frame_form = tk.LabelFrame(
            self, text=" Data Mahasiswa ", font=("Arial", 11, "bold"),
            padx=15, pady=15, bg="#f0f0f0"
        )
        frame_form.pack(fill="x", padx=20, pady=(0, 10))

        # Baris 1: NIM & Jurusan
        tk.Label(frame_form, text="NIM", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_nim = tk.Entry(frame_form, width=25, font=("Arial", 10))
        self.ent_nim.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Jurusan", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=2, sticky="w", pady=5, padx=(30, 0))
        self.cmb_jurusan = ttk.Combobox(
            frame_form,
            values=["Teknik Informatika", "Sistem Informasi", "Teknik Elektro", "Manajemen", "Akuntansi"],
            state="readonly", width=23, font=("Arial", 10)
        )
        self.cmb_jurusan.grid(row=0, column=3, pady=5, padx=5)

        # Baris 2: Nama & Tahun
        tk.Label(frame_form, text="Nama", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_nama = tk.Entry(frame_form, width=25, font=("Arial", 10))
        self.ent_nama.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Tahun", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=2, sticky="w", pady=5, padx=(30, 0))
        self.ent_tahun = tk.Entry(frame_form, width=25, font=("Arial", 10))
        self.ent_tahun.grid(row=1, column=3, pady=5, padx=5)

        # ==================== TOMBOL AKSI ====================
        frame_btn = tk.Frame(self, bg="#f0f0f0")
        frame_btn.pack(pady=(5, 10))

        self.btn_simpan = tk.Button(
            frame_btn, text="Daftarkan", bg="#003366", fg="white",
            width=12, font=("Arial", 10, "bold"), cursor="hand2"
        )
        self.btn_simpan.pack(side="left", padx=8)

        self.btn_update = tk.Button(
            frame_btn, text="Update", bg="#CC8400", fg="white",
            width=12, font=("Arial", 10, "bold"), cursor="hand2"
        )
        self.btn_update.pack(side="left", padx=8)

        self.btn_hapus = tk.Button(
            frame_btn, text="Hapus", bg="#CC0000", fg="white",
            width=12, font=("Arial", 10, "bold"), cursor="hand2"
        )
        self.btn_hapus.pack(side="left", padx=8)

        self.btn_clear = tk.Button(
            frame_btn, text="Bersihkan Form", bg="#555555", fg="white",
            width=14, font=("Arial", 10, "bold"), cursor="hand2"
        )
        self.btn_clear.pack(side="left", padx=8)

        # ==================== TABEL TREEVIEW ====================
        frame_tabel = tk.Frame(self, bg="#f0f0f0")
        frame_tabel.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        columns = ("nim", "nama", "jurusan", "tahun")
        self.tree = ttk.Treeview(frame_tabel, columns=columns, show="headings")
        self.tree.heading("nim", text="NIM")
        self.tree.heading("nama", text="NAMA")
        self.tree.heading("jurusan", text="JURUSAN")
        self.tree.heading("tahun", text="TAHUN")

        self.tree.column("nim", width=120, anchor="center")
        self.tree.column("nama", width=220, anchor="center")
        self.tree.column("jurusan", width=180, anchor="center")
        self.tree.column("tahun", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_form_data(self):
        return (
            self.ent_nim.get().strip(),
            self.ent_nama.get().strip(),
            self.cmb_jurusan.get().strip(),
            self.ent_tahun.get().strip()
        )

    def get_search_keyword(self):
        return self.ent_search.get().strip()

    def clear_form(self):
        self.ent_nim.config(state="normal")
        self.ent_nim.delete(0, tk.END)
        self.ent_nama.delete(0, tk.END)
        self.cmb_jurusan.set('')
        self.ent_tahun.delete(0, tk.END)

    def load_to_form(self, nim, nama, jurusan, tahun):
        self.clear_form()
        self.ent_nim.insert(0, nim)
        self.ent_nim.config(state="readonly")  # Kunci PK saat update
        self.ent_nama.insert(0, nama)
        self.cmb_jurusan.set(jurusan)
        self.ent_tahun.insert(0, tahun)

# ==========================================
# [Pertemuan 6: Pewarisan Sifat (Inheritance)]
# Class MainView mewarisi properti dari tk.Tk (Window utama)
# ==========================================
class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIAKAD - Sistem Manajemen Mahasiswa")
        self.geometry("900x600")
        self.minsize(800, 550)
        
        # Container untuk menumpuk frame (Frame Switching)
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (DashboardFrame, FormMahasiswaFrame):
            frame = F(self.container)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew") # Stack frame di koordinat grid yang sama

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self)
        
        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Keluar", command=self.quit)
        menubar.add_cascade(label="File", menu=menu_file)
        
        menu_nav = tk.Menu(menubar, tearoff=0)
        menu_nav.add_command(label="Dashboard", command=lambda: self.show_frame("DashboardFrame"))
        menu_nav.add_command(label="Kelola Data Mahasiswa", command=lambda: self.show_frame("FormMahasiswaFrame"))
        menubar.add_cascade(label="Navigasi", menu=menu_nav)

        menu_bantuan = tk.Menu(menubar, tearoff=0)
        menu_bantuan.add_command(label="Info Aplikasi", command=lambda: messagebox.showinfo("Info", "SIAKAD Mini v1.0\nMenggunakan teknik Frame Switching."))
        menubar.add_cascade(label="Bantuan", menu=menu_bantuan)

        self.config(menu=menubar)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() # Teknik Frame Switching memunculkan frame ke atas
