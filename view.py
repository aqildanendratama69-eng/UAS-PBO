# view.py
import tkinter as tk
from tkinter import ttk, messagebox

class DashboardFrame(tk.Frame):
    """Menerapkan Inheritance dari tk.Frame"""
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg="#f4f6f9")
        
        label_judul = tk.Label(self, text="Sistem Informasi Akademik (SIAKAD)", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#333")
        label_judul.pack(pady=40)
        
        label_sub = tk.Label(self, text="Selamat Datang di Aplikasi Manajemen Data Mahasiswa\nGunakan Menu Bar di atas untuk menavigasi aplikasi.", font=("Arial", 12), bg="#f4f6f9", justify="center")
        label_sub.pack(pady=10)

class FormMahasiswaFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg="#ffffff")
        self.setup_ui()

    def setup_ui(self):
        # Frame Form Input
        frame_form = tk.LabelFrame(self, text=" Form Input / Edit Mahasiswa ", font=("Arial", 11, "bold"), padx=15, pady=15, bg="#ffffff")
        frame_form.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_form, text="NIM (PK):", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_nim = tk.Entry(frame_form, width=25)
        self.ent_nim.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Nama Lengkap:", bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_nama = tk.Entry(frame_form, width=35)
        self.ent_nama.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Jurusan / Prodi:", bg="#ffffff").grid(row=0, column=2, sticky="w", pady=5, padx=(20,0))
        self.cmb_jurusan = ttk.Combobox(frame_form, values=["Informatika", "Sistem Informasi", "Teknik Elektro", "Manajemen"], state="readonly", width=22)
        self.cmb_jurusan.grid(row=0, column=3, pady=5, padx=5)

        tk.Label(frame_form, text="IPK (0.00 - 4.00):", bg="#ffffff").grid(row=1, column=2, sticky="w", pady=5, padx=(20,0))
        self.ent_ipk = tk.Entry(frame_form, width=25)
        self.ent_ipk.grid(row=1, column=3, pady=5, padx=5)

        # Tombol Aksi
        frame_btn = tk.Frame(frame_form, bg="#ffffff")
        frame_btn.grid(row=2, column=0, columnspan=4, pady=15)

        self.btn_simpan = tk.Button(frame_btn, text="Simpan Baru", bg="#28a745", fg="white", width=12, font=("Arial", 9, "bold"))
        self.btn_simpan.pack(side="left", padx=5)

        self.btn_update = tk.Button(frame_btn, text="Update Data", bg="#007bff", fg="white", width=12, font=("Arial", 9, "bold"))
        self.btn_update.pack(side="left", padx=5)

        self.btn_hapus = tk.Button(frame_btn, text="Hapus Data", bg="#dc3545", fg="white", width=12, font=("Arial", 9, "bold"))
        self.btn_hapus.pack(side="left", padx=5)

        self.btn_clear = tk.Button(frame_btn, text="Reset Form", bg="#6c757d", fg="white", width=12, font=("Arial", 9, "bold"))
        self.btn_clear.pack(side="left", padx=5)

        # Tabel Treeview
        frame_tabel = tk.Frame(self)
        frame_tabel.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("nim", "nama", "jurusan", "ipk")
        self.tree = ttk.Treeview(frame_tabel, columns=columns, show="headings")
        self.tree.heading("nim", text="NIM")
        self.tree.heading("nama", text="Nama Mahasiswa")
        self.tree.heading("jurusan", text="Jurusan")
        self.tree.heading("ipk", text="IPK")

        self.tree.column("nim", width=120, anchor="center")
        self.tree.column("nama", width=250)
        self.tree.column("jurusan", width=180)
        self.tree.column("ipk", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_form_data(self):
        return (self.ent_nim.get().strip(), self.ent_nama.get().strip(), self.cmb_jurusan.get(), self.ent_ipk.get().strip())

    def clear_form(self):
        self.ent_nim.config(state="normal")
        self.ent_nim.delete(0, tk.END)
        self.ent_nama.delete(0, tk.END)
        self.cmb_jurusan.set('')
        self.ent_ipk.delete(0, tk.END)

    def load_to_form(self, nim, nama, jurusan, ipk):
        self.clear_form()
        self.ent_nim.insert(0, nim)
        self.ent_nim.config(state="readonly")  # Kunci PK saat update
        self.ent_nama.insert(0, nama)
        self.cmb_jurusan.set(jurusan)
        self.ent_ipk.insert(0, ipk)

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIAKAD - Sistem Informasi Akademik Mini (OOP MVC)")
        self.geometry("800x550")
        self.minsize(700, 500)
        
        # Container untuk menumpuk frame
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
        menu_bantuan.add_command(label="Info Aplikasi", command=lambda: messagebox.showinfo("Info", "SIAKAD Mini v1.0\nProyek PBO Berbasis Strict MVC."))
        menubar.add_cascade(label="Bantuan", menu=menu_bantuan)

        self.config(menu=menubar)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() # Teknik Frame Switching