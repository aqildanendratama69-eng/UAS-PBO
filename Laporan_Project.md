# Laporan Project UAS PBO - Sistem Informasi Akademik (SIAKAD)

## 1. Deskripsi Aplikasi
Aplikasi SIAKAD (Sistem Informasi Akademik) adalah sebuah aplikasi berbasis Desktop yang dibangun menggunakan bahasa pemrograman Python dan antarmuka Graphical User Interface (GUI) Tkinter. Aplikasi ini dirancang untuk memanajemen data akademik secara efisien dan menerapkan konsep Pemrograman Berorientasi Objek (PBO/OOP).

Aplikasi ini menggunakan arsitektur **Model-View-Controller (MVC)** untuk memisahkan antara logika data (Database/SQLite), antarmuka pengguna (GUI Tkinter), dan logika kontrol aplikasi.

## 2. Fitur-Fitur Utama Aplikasi
Aplikasi ini telah diperbarui dengan berbagai fitur profesional, di antaranya:
1.  **Sistem Autentikasi (Login)**
    *   Sistem login aman menggunakan database SQLite.
    *   Hanya pengguna dengan kredensial yang valid (Contoh: `admin` / `admin123`) yang dapat masuk ke dalam dashboard.
2.  **Dashboard Interaktif**
    *   Menampilkan ringkasan data statistik akademik secara *real-time* menggunakan kartu-kartu informasi.
    *   Data mencakup: Total Mahasiswa, Total Mata Kuliah, dan Total Transaksi KRS.
3.  **Kelola Data Mahasiswa (CRUD Lengkap)**
    *   Tambah, Baca, Ubah, dan Hapus data Mahasiswa.
    *   Fitur pencarian mahasiswa berdasarkan NIM, Nama, atau Jurusan.
4.  **Pengisian Kartu Rencana Studi (KRS) & CRUD Mata Kuliah**
    *   Fitur untuk menambahkan daftar Mata Kuliah ke dalam sistem.
    *   Pengisian KRS yang terhubung langsung dengan relasi *Many-to-Many* di database (Tabel Cascade).
    *   **Validasi SKS Cerdas:** Sistem akan secara otomatis menolak jika mahasiswa mengambil lebih dari batas maksimal (24 SKS).
5.  **Input Nilai Semester**
    *   Fitur khusus bagi admin/dosen untuk memberikan nilai (A, B, C, D, E) pada mata kuliah yang telah diambil mahasiswa di KRS.
6.  **Desain UI Modern (Estetika)**
    *   Menggunakan modul `ttk.Style` untuk mempercantik font, padding, dan warna tombol.
    *   Tabel data menggunakan *Zebra Striping* (warna selang-seling) agar mudah dibaca.

## 3. Penerapan Konsep PBO (OOP)
Aplikasi ini menerapkan 4 pilar utama Pemrograman Berorientasi Objek:
1.  **Encapsulation (Pengkapsulan):** 
    Menyembunyikan atribut sensitif dengan tanda *double underscore* (`__nim`, `__jurusan`) di dalam class `Mahasiswa` agar tidak bisa diubah langsung dari luar, melainkan harus menggunakan *getter* dan *setter*.
2.  **Inheritance (Pewarisan Sifat):** 
    Class `Mahasiswa` mewarisi (inherits) sifat dari *Abstract Base Class* `Person`. Begitu juga pada *View*, semua class Frame seperti `LoginFrame`, `DashboardFrame` mewarisi `tk.Frame`.
3.  **Polymorphism (Polimorfisme):** 
    Implementasi (overriding) dari *method* abstrak `get_role()` di dalam class `Mahasiswa` yang berbeda perlakuannya dibandingkan jika dipanggil dari entitas turunan `Person` lainnya.
4.  **Abstraction (Abstraksi):** 
    Pembuatan class abstrak `Person` menggunakan modul `abc` di Python, yang memberikan kerangka dasar (*blueprint*) method yang wajib dimiliki oleh subclass-nya.

## 4. Struktur Database (SQLite)
Database menggunakan file `siakad.db` dengan 4 tabel utama:
1.  **`users`**: Menyimpan kredensial admin (id, username, password, role).
2.  **`mahasiswa`**: Menyimpan data identitas (nim, nama, jurusan, tahun).
3.  **`mata_kuliah`**: Menyimpan katalog matkul (kode_mk, nama_mk, sks).
4.  **`krs`**: Tabel perantara (Many-to-Many) yang menyimpan nim, kode_mk, serta kolom nilai.

## 5. Kesimpulan
Proyek ini berhasil mendemonstrasikan perpaduan antara logika database relasional, antarmuka pengguna grafis, dan praktik penerapan arsitektur OOP yang rapi di dalam bahasa Python. Aplikasi SIAKAD ini sudah siap digunakan sebagai simulasi manajemen akademik tingkat universitas.
