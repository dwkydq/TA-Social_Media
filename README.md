# Mini X - Social Media App

Aplikasi media sosial berbasis web dengan fitur real-time chat, posting media, like, komentar, dan sistem follow. Dibangun menggunakan Python Flask dan MySQL.

---

## Daftar Isi

- [Prasyarat](#prasyarat)
- [Instalasi dan Setup](#instalasi-dan-setup)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Struktur Project](#struktur-project)
- [Fitur Utama](#fitur-utama)

---

## Prasyarat

- **Python 3.x**
- **pip** (Python Package Installer)
- **MySQL Server** (XAMPP / Laragon)
- **Git** (Opsional)

---

## Instalasi dan Setup
Ikuti langkah-langkah berikut untuk menyiapkan project dari awal:

### 1. Clone Project
```bash
git clone [https://github.com/dwkydq/TA-Social_Media.git](https://github.com/dwkydq/TA-Social_Media.git)
cd TA-Social_Media
```

### 2. Buat Virtual Environment
Disarankan menggunakan virtual environment agar library tidak tercampur dengan sistem global.
```
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### 3. Aktifkan Virtual Environment
Langkah ini wajib dilakukan setiap kali akan menjalankan project.
```
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 4. Install Dependencies
Install semua library yang dibutuhkan yang terdaftar di `requirements.txt`.
```
pip install -r requirements.txt
```

### 5. Konfigurasi Environment (.env)
Buat file baru bernama `.env` di folder utama (sejajar dengan `run.py`), lalu isi konfigurasi berikut:
```
SECRET_KEY=rahasia_kunci_anda_disini
DATABASE_URI=mysql+pymysql://root:@localhost/socialmedia
```
(Catatan: Sesuaikan `root` dan password database jika ada. Format: `user:password@host/nama_db`)

### 6. Setup Database
Pastikan MySQL (XAMPP/Laragon) sudah berjalan, lalu buat database kosong.
1. Buka phpMyAdmin atau terminal MySQL.
2. Jalankan query:
```
CREATE DATABASE socialmedia;
```
3. Tabel akan otomatis dibuat oleh SQLAlchemy saat aplikasi pertama kali dijalankan (jika kode `db.create_all()` sudah ada di `__init__.py`).

---

## Menjalankan Aplikasi
Pastikan virtual environment sudah aktif, lalu jalankan perintah:
```
python run.py
```
Aplikasi akan berjalan di http://127.0.0.1:5000/.

---

## Struktur Project
Berikut adalah struktur direktori project beserta penjelasannya:
```
TA-Social_Media/
├── app/                        # Folder utama aplikasi
│   ├── templates/              # File HTML (Frontend)
│   │   ├── base.html           # Layout utama
│   │   ├── home.html           # Halaman beranda
│   │   ├── chat.html           # Halaman chat room
│   │   └── ...                 
│   ├── static/                 # File CSS, JS, dan Uploads
│   │   ├── style.css
│   │   ├── chat.js             # Logic Socket.IO Client
│   │   └── uploads/            # Penyimpanan gambar user
│   ├── __init__.py             # Inisialisasi Flask, SQLAlchemy, LoginManager
│   ├── models.py               # Definisi Tabel Database (User, Post, Chat)
│   └── routes.py               # Logika Routing & Controller
├── venv/                       # Virtual Environment
├── .env                        # Konfigurasi sensitif (Database & Secret Key)
├── requirements.txt            # Daftar library (Flask, SQLAlchemy, dll)
├── run.py                      # Entry point aplikasi
└── README.md                   # Dokumentasi ini
```
### Penjelasan File Penting:
- **run.py:** Pintu masuk aplikasi. Menjalankan server Flask dengan dukungan Socket.IO.
- **app/__init__.py:** Tempat konfigurasi aplikasi, inisialisasi koneksi database (`db`), dan login manager.
- **app/models.py:** Representasi tabel database dalam bentuk Class Python (ORM). Contoh: Class `User`, `Post`, `Chat`.
- **app/routes.py:** Mengatur alur halaman. Contoh: Jika user akses `/profile`, file ini mengambil data dari database lalu melemparnya ke `profile.html`.
- **app/templates/:** Berisi tampilan antarmuka (UI) menggunakan Jinja2.

---

## Fitur Utama
Berikut adalah daftar fitur dan routing yang tersedia dalam aplikasi:

### 1. Autentikasi User
- **Login:** `/login` (POST/GET) - Masuk menggunakan email & password.
- **Register:** `/register` (POST/GET) - Pendaftaran akun baru.
- **Logout:** `/logout` - Keluar dari sesi.

### 2. Posting & Timeline
- **Home:** `/` - Menampilkan feed postingan terbaru dari semua user.
- **Create Post:** `/post` (POST) - Upload foto/video dengan caption.
- **Delete Post:** `/delete_post/<id>` - Menghapus postingan sendiri.

### 3. Interaksi
- **Like Post:** `/like/<id>` - Menyukai postingan.
- **Comment:** `/comment/<id>` - Memberikan komentar pada postingan.
- **Follow:** `/follow/<id>` - Mengikuti user lain.

### 4. Real-time Chat
- **Chat Room:** `/chat/<user_id>`
    - Menggunakan **Socket.IO** untuk komunikasi dua arah.
    - Pesan tersimpan otomatis di database.
    - Mendukung fitur typing indicator.
- **Chat list:** `/chat_list` - Melihat daftar riwayat percakapan.

### 5. Profil & Pencarian
- **Profile:** `/profile/<id>` - Melihat bio, followers, following, dan postingan user.
- **Edit Profile:** `/edit-profile` - Mengubah foto profil, nama, dan bio.
- **Search:** `/search?q=keyword` - Mencari user berdasarkan username.

---

## Dokumentasi API
### Get All Users
**GET** `/users`
```
{
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  ],
  "message": ""
}
```
### Create User
**POST** `/users`

```
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secretpassword"
}
```

### Get User Detail
**GET** `/users/<id>`


### Update User
**PUT** `/users/<id>`

### Delete User
**DELETE** `/users/<id>`
