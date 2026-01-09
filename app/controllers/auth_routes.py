from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import db
from app.models import User
import os

# Membuat Blueprint 'auth'
auth_bp = Blueprint('auth', __name__)

# --- 1. FITUR REGISTER ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.home'))

    if request.method == 'POST':
        # Ambil data dari Form HTML
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Cek apakah email sudah terdaftar
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email sudah terdaftar! Gunakan email lain.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Cek apakah username sudah terdaftar
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash('Username sudah dipakai! Pilih username lain.', 'danger')
            return redirect(url_for('auth.register'))

        # Logika Upload Foto Profil (Opsional)
        filename = None
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        # Enkripsi Password (Hashing) agar aman
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Buat User Baru
        new_user = User(name=name, username=username, email=email, password=hashed_password, profile_pic=filename)
        
        # Simpan ke Database
        db.session.add(new_user)
        db.session.commit()

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


# --- 2. FITUR LOGIN ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Jika user sudah login, lempar ke home
    if current_user.is_authenticated:
        return redirect(url_for('frontend.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Cari user berdasarkan email
        user = User.query.filter_by(email=email).first()

        # Cek password
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login berhasil! Selamat datang.', 'success')
            
            # Cek apakah user tadi mau ke halaman tertentu (misal dipaksa login saat buka profil)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('frontend.home'))
        else:
            flash('Login gagal. Periksa email dan password Anda.', 'danger')

    return render_template('auth/login.html')


# --- 3. FITUR LOGOUT ---
@auth_bp.route('/logout')
@login_required 
def logout():
    logout_user()
    flash('Anda telah keluar.', 'info')
    return redirect(url_for('auth.login'))