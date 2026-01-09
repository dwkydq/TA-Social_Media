# Mini X - Social Media App Aplikasi media sosial berbasis web dengan fitur real-time chat, posting media, like, komentar, dan sistem follow. Dibangun menggunakan Python Flask dan MySQL. ## Daftar Isi - [Prasyarat](#prasyarat) - [Instalasi dan Setup](#instalasi-dan-setup) - [Menjalankan Aplikasi](#menjalankan-aplikasi) - [Struktur Project](#struktur-project) - [Fitur Utama](#fitur-utama) ## Prasyarat - **Python 3.x** - **pip** (Python Package Installer) - **MySQL Server** (XAMPP / Laragon) - **Git** (Opsional) ## Instalasi dan Setup Ikuti langkah-langkah berikut untuk menyiapkan project dari awal: ### 1. Clone Project
bash
git clone [https://github.com/dwkydq/TA-Social_Media.git](https://github.com/dwkydq/TA-Social_Media.git)
cd TA-Social_Media
2. Buat Virtual Environment
Disarankan menggunakan virtual environment agar library tidak tercampur dengan sistem global.

Bash

# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
3. Aktifkan Virtual Environment
Langkah ini wajib dilakukan setiap kali akan menjalankan project.

Bash

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
4. Install Dependencies
Install semua library yang dibutuhkan yang terdaftar di requirements.txt.

Bash

pip install -r requirements.txt
5. Konfigurasi Environment (.env)
Buat file baru bernama .env di folder utama (sejajar dengan run.py), lalu isi konfigurasi berikut:

Cuplikan kode

SECRET_KEY=rahasia_kunci_anda_disini
DATABASE_URI=mysql+pymysql://root:@localhost/socialmedia
(Catatan: Sesuaikan root dan password database jika ada. Format: user:password@host/nama_db)

6. Setup Database
Pastikan MySQL (XAMPP/Laragon) sudah berjalan, lalu buat database kosong.

Buka phpMyAdmin atau terminal MySQL.

Jalankan query:

SQL

CREATE DATABASE socialmedia;
Tabel akan otomatis dibuat oleh SQLAlchemy saat aplikasi pertama kali dijalankan.

Menjalankan Aplikasi
Pastikan virtual environment sudah aktif, lalu jalankan perintah:

Bash

python run.py
Aplikasi akan berjalan di http://127.0.0.1:5000/.

Struktur Project
Berikut adalah struktur direktori project beserta penjelasannya:

Plaintext

TA-Social_Media/
├── app/                        # Folder utama aplikasi
│   ├── templates/              # File HTML (Frontend)
│   ├── static/                 # File CSS, JS, dan Uploads
│   ├── __init__.py             # Inisialisasi Flask & DB
│   ├── models.py               # Definisi Tabel Database (User, Post, Chat)
│   └── routes.py               # Logika Routing & Controller
├── venv/                       # Virtual Environment
├── .env                        # Konfigurasi sensitif
├── requirements.txt            # Daftar library
├── run.py                      # Entry point aplikasi
└── README.md                   # Dokumentasi ini
Fitur Utama
Autentikasi: Login & Register aman.

Posting: Upload foto/video dengan caption.

Interaksi: Like & Komentar.

Real-time Chat: Pesan instan menggunakan Socket.IO.

Profil: Edit profil dan follow user lain.


### Langkah 3: Simpan (Commit)

Setelah nama file diubah menjadi `README.md` dan isinya diganti dengan kode di atas:
1.  Gulir ke bawah ke bagian **Commit changes**.
2.  Tulis pesan commit, misal: "Fix README formatting".
3.  Klik tombol hijau **Commit changes**.
