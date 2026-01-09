import os

class Config:
    # 1. Setup Path Absolut
    # Ini mencegah error "File not found" jika aplikasi dijalankan dari folder berbeda
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Setup folder upload (foto profil/postingan)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-tako-twitter'

    # 2. Setup Database
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASS = ''    
    DB_NAME = 'social_media_app'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False