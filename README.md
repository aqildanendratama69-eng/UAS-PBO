# 🎓 Sistem Informasi Akademik Mini (SIAKAD)

> **Proyek Akhir Mata Kuliah Pemrograman Berbasis Objek (PBO)**  
> Aplikasi Desktop Berbasis Python (Tkinter), Database SQLite, dan Arsitektur Strict MVC.

---

## 📌 Deskripsi Proyek
**SIAKAD Mini** adalah aplikasi pengelolaan data akademik mahasiswa tingkat menengah (*enterprise-grade prototype*) berbasis desktop. Aplikasi ini dirancang dengan menerapkan konsep rekayasa perangkat lunak bermutu tinggi, termasuk penataan kode berbasis objek secara ketat, enkapsulasi data, arsitektur **Model-View-Controller (MVC)**, serta navigasi multi-halaman dalam satu jendela utama (*Single Page Application*).

---

## 🚀 Fitur Utama
* **Dashboard Navigasi:** Halaman selamat datang dengan petunjuk penggunaan menu interaktif.
* **Fitur CRUD Terintegrasi Database SQLite:**
  * **Create:** Menambahkan data mahasiswa baru beserta validasi tipe data (NIM, Nama, Jurusan, IPK).
  * **Read:** Menampilkan daftar seluruh data mahasiswa ke dalam tabel `ttk.Treeview` secara real-time.
  * **Update:** Memilih baris data pada tabel (klik ganda), mengunci kunci utama (*Primary Key/NIM*), dan memperbarui informasi.
  * **Delete:** Menghapus data mahasiswa secara permanen setelah melalui dialog konfirmasi (`askyesno`).
* **Multi-Page Navigation:** Peralihan halaman tanpa *popup spam* menggunakan teknik *Frame Switching* (`.tkraise()`).
* **Exception Handling & Validation:** Penanganan kesalahan input (seperti karakter pada kolom IPK atau duplikasi NIM) menggunakan dialog notifikasi `messagebox` tanpa membuat aplikasi *crash*.

---

## 🛠️ Pemetaan Konsep PBO & Materi Kuliah

| Pertemuan / Konsep | Penerapan dalam Kode Program |
| :--- | :--- |
| **Pertemuan 2: Class & Objek** | Penentuan skema data `Mahasiswa` dan `DatabaseModel` di `model.py`. |
| **Pertemuan 3: Method & `self`** | Penggunaan parameter `self` di setiap *instance method* seluruh modul. |
| **Pertemuan 4: Encapsulation** | Penggunaan *private attributes* (`self.__nim`, `self.__nama`, dll.) serta fungsi *Getter* dan *Setter*. |
| **Pertemuan 5: Relasi Antar Objek** | Objek `Controller` menghubungkan dan mengontrol komunikasi antara `DatabaseModel` dan `MainView`. |
| **Pertemuan 6: Inheritance** | Class antarmuka (`DashboardFrame`, `FormMahasiswaFrame`) mewarisi sifat dari `tk.Frame`. |
| **Pertemuan 7: Polymorphism** | Inisialisasi dan penumpukan *frame* seragam melalui *looping* class di `MainView`. |
| **Pertemuan 9: Abstraksi** | Menyembunyikan kompleksitas query SQL dari Controller melalui metode sederhana `get_all_mahasiswa()`. |
| **Pertemuan 10: Exception Handling** | Blok `try-except-finally` untuk menangkap `sqlite3.IntegrityError` dan `ValueError`. |
| **Pertemuan 11: SQLite CRUD** | Persistensi data permanen di file `siakad.db` dengan query SQL terisolasi di `model.py`. |
| **Pertemuan 12: GUI Tkinter & Layout** | Penggunaan layout manager `grid()` dan `pack()` secara proporsional. |
| **Pertemuan 13: Event Handling** | Merekam aksi tombol dan klik ganda tabel (`tree.bind("<Double-1>", ...)`) ke Controller. |

---

## 📁 Struktur Direktori
```text
PROYEK_PBO_SIAKAD/
│
├── model.py     # Lapisan Data & OOP (Database SQLite & Class Mahasiswa)
├── view.py      # Lapisan Antarmuka (Komponen Visual Tkinter & Multi-Frame)
├── main.py      # Lapisan Controller / Router (Penghubung Model & View)
├── siakad.db    # Database SQLite Lokal (Dibuat otomatis)
└── README.md    # Dokumentasi Proyek