from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Post, User, Notification, Follow
from sqlalchemy.sql import func

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')

@frontend_bp.route('/home')
@login_required
def home():
    # --- LOGIKA FILTER BERANDA ---
    
    # 1. Ambil daftar orang yang saya follow
    followed_follows = current_user.following.all() 
    
    # 2. Ambil ID user yang di-follow saja (list comprehension)
    followed_ids = [f.followed_id for f in followed_follows]

    # 3. Masukkan ID saya sendiri (supaya postingan sendiri juga muncul di beranda)
    followed_ids.append(current_user.id)

    # 4. Query ke Database dengan Filter:
    posts = Post.query.filter(Post.user_id.in_(followed_ids))\
                      .order_by(Post.created_at.desc())\
                      .all()

    return render_template('main/feed.html', posts=posts)

@frontend_bp.route('/explore')
def explore():
    # Tampilkan post secara acak (Untuk halaman Jelajah)
    posts = Post.query.order_by(func.random()).limit(20).all()
    return render_template('main/explore.html', posts=posts)

@frontend_bp.route('/notifications')
@login_required
def notifications():
    # Ambil notifikasi milik user login, urutkan dari terbaru
    notifs = Notification.query.filter_by(user_id=current_user.id)\
             .order_by(Notification.created_at.desc()).all()
    return render_template('main/notifications.html', notifications=notifs)

@frontend_bp.route('/search')
def search():
    query = request.args.get('q')
    if query:
        # Cari user berdasarkan username atau nama
        users = User.query.filter((User.username.like(f'%{query}%')) | (User.name.like(f'%{query}%'))).all()
        return render_template('main/search.html', users=users, query=query)
    return render_template('main/search.html', users=[], query=None)