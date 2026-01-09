# Flask REST API Project

Project ini adalah aplikasi REST API berbasis **Python Flask** dengan struktur MVC, database menggunakan **SQLAlchemy**, migrasi dengan **Flask-Migrate**, dan testing menggunakan **pytest**.

---

## Daftar Isi

- [Prasyarat](#prasyarat)
- [Instalasi dan Setup](#instalasi-dan-setup)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Menjalankan Testing](#menjalankan-testing)
- [Struktur Project](#struktur-project)
- [Dokumentasi API](#dokumentasi-api)

---

## Prasyarat

Pastikan sudah terinstall:

- **Python 3.x**
- **pip** (Python Package Installer)
- **Git** (Opsional)

---

## Instalasi dan Setup

Ikuti langkah-langkah berikut untuk menyiapkan project dari awal.

### 1. Clone atau Download Project

```bash
git clone <repository-url>
cd <folder-project>
2. Buat Virtual Environment
Disarankan menggunakan virtual environment agar library tidak tercampur dengan sistem global.

bash
Copy code
# Windows
python -m venv venv

# Linux / Mac
python3 -m venv venv
3. Aktifkan Virtual Environment
Langkah ini wajib dilakukan setiap kali akan menjalankan project.

bash
Copy code
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / Mac
source venv/bin/activate
4. Install Dependencies
Install semua library yang dibutuhkan yang terdaftar di requirements.txt.

bash
Copy code
pip install -r requirements.txt
5. Setup Database (Migrasi)
Inisialisasi dan jalankan migrasi database untuk membuat tabel.

bash
Copy code
# Inisialisasi folder migrations (jika belum ada)
flask db init

# Membuat file migrasi berdasarkan model
flask db migrate -m "Initial migration"

# Menerapkan migrasi ke database (membuat tabel)
flask db upgrade
Menjalankan Aplikasi
Pastikan virtual environment sudah aktif, lalu jalankan:

bash
Copy code
flask run
Atau menggunakan Python langsung:

bash
Copy code
python main.py
Aplikasi akan berjalan di:

cpp
Copy code
http://127.0.0.1:5000/
Menjalankan Testing
Project ini menggunakan pytest untuk unit testing.

bash
Copy code
pytest
Struktur Project
plaintext
Copy code
PYTHON/
├── app/
│   ├── controller/
│   │   ├── __init__.py
│   │   └── UserController.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── todo.py
│   │   └── user.py
│   ├── __init__.py
│   ├── response.py
│   └── routes.py
├── migrations/
├── tests/
│   ├── conftest.py
│   └── test_user.py
├── venv/
├── .flaskenv
├── app.db
├── config.py
├── main.py
├── pytest.ini
└── requirements.txt
Dokumentasi API
Get All Users
URL: /users
Method: GET

json
Copy code
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
Create User
URL: /users
Method: POST

json
Copy code
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secretpassword"
}
Get User Detail
URL: /users/<id>
Method: GET

Update User
URL: /users/<id>
Method: PUT

Delete User
URL: /users/<id>
Method: DELETE

yaml
Copy code

---

## ✅ Cara Pakai di GitHub

1. Buka repository kamu  
2. Klik `README.md`  
3. Klik ✏️ **Edit**  
4. Hapus semua isi lama  
5. **Paste teks di atas**  
6. Klik **Commit changes**

---

Kalau kamu mau, saya juga bisa:

✨ Tambahin Swagger  
✨ Tambahin ERD  
✨ Tambahin Screenshot  
✨ Buat versi Bahasa Inggris  
✨ Buat dokumentasi API lengkap  

Tinggal bilang mau yang mana 😎






You said:

kenapa jadinya seperti ini?

ChatGPT said:
Masalahnya bukan di GitHub, tapi di format Markdown README kamu yang rusak karena:

❌ Penyebab Utama
Code block tidak ditutup dengan benar
Contoh yang salah:

markdown
Copy code
`bash git clone cd
Harusnya:

markdown
Copy code
```bash
git clone ...
cd ...
Copy code
Judul & daftar tidak dipisah baris kosong
Markdown butuh spasi/baris kosong agar rapi.

Campur antara inline code (`) dan code block (```)
Akibatnya teks tampil aneh seperti di screenshot.

✅ Solusi: Gunakan README yang Sudah Benar
Silakan hapus semua isi README lama, lalu paste 100% teks di bawah ini:

🔽 COPY SEMUA DARI SINI 🔽
markdown
Copy code
# Flask REST API Project

Project ini adalah aplikasi REST API berbasis **Python Flask** dengan struktur MVC, database menggunakan **SQLAlchemy**, migrasi dengan **Flask-Migrate**, dan testing menggunakan **pytest**.

---

## Daftar Isi

- [Prasyarat](#prasyarat)
- [Instalasi dan Setup](#instalasi-dan-setup)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Menjalankan Testing](#menjalankan-testing)
- [Struktur Project](#struktur-project)
- [Dokumentasi API](#dokumentasi-api)

---

## Prasyarat

Pastikan sudah terinstall:

- **Python 3.x**
- **pip** (Python Package Installer)
- **Git** (Opsional)

---

## Instalasi dan Setup

Ikuti langkah-langkah berikut untuk menyiapkan project dari awal.

### 1. Clone atau Download Project

```bash
git clone <repository-url>
cd <folder-project>
2. Buat Virtual Environment
Disarankan menggunakan virtual environment agar library tidak tercampur dengan sistem global.

Windows

bash
Copy code
python -m venv venv
Linux / Mac

bash
Copy code
python3 -m venv venv
3. Aktifkan Virtual Environment
bash
Copy code
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / Mac
source venv/bin/activate
4. Install Dependencies
bash
Copy code
pip install -r requirements.txt
5. Setup Database
bash
Copy code
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Menjalankan Aplikasi
bash
Copy code
flask run
Atau:

bash
Copy code
python main.py
Aplikasi berjalan di:

cpp
Copy code
http://127.0.0.1:5000/
Menjalankan Testing
bash
Copy code
pytest
Struktur Project
plaintext
Copy code
PYTHON/
├── app/
│   ├── controller/
│   ├── model/
│   ├── response.py
│   └── routes.py
├── migrations/
├── tests/
├── venv/
├── config.py
├── main.py
└── requirements.txt
Dokumentasi API
Get All Users
GET /users

json
Copy code
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
Create User
POST /users

json
Copy code
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secretpassword"
}
Get User Detail
GET /users/<id>

Update User
PUT /users/<id>

Delete User
DELETE /users/<id>
