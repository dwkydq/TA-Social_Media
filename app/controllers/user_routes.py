from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Notification, Post, PostLike
import os

user_bp = Blueprint('user', __name__)

# 1. Redirect ke Profil Sendiri
@user_bp.route('/profile')
@login_required
def my_profile():
    return redirect(url_for('user.profile', username=current_user.username))

# 2. Tampilkan Profil (DENGAN LOGIKA TAB)
@user_bp.route('/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    # Ambil parameter tab dari URL (default: 'posts')
    active_tab = request.args.get('tab', 'posts')
    
    # --- LOGIKA FILTER BERDASARKAN TAB ---
    if active_tab == 'likes':
        posts = Post.query.join(PostLike, (PostLike.post_id == Post.id)) \
                          .filter(PostLike.user_id == user.id) \
                          .order_by(PostLike.created_at.desc()) \
                          .all()
                          
    elif active_tab == 'media':
        # Ambil postingan user ini yang PUNYA GAMBAR/VIDEO
        posts = Post.query.filter_by(user_id=user.id) \
                          .filter(Post.media_url != None) \
                          .order_by(Post.created_at.desc()) \
                          .all()
                          
    else: # Default: Tab Postingan
        # Ambil semua postingan user ini
        posts = Post.query.filter_by(user_id=user.id) \
                          .order_by(Post.created_at.desc()) \
                          .all()

    # Hitung Statistik untuk Header Profil
    followers_count = user.followers.count()
    following_count = user.following.count()
    
    # Cek status follow
    is_following = False
    if current_user.is_authenticated and current_user.id != user.id:
        is_following = current_user.is_following(user)
    
    return render_template('main/profile.html', 
                           user=user, 
                           posts=posts,              
                           active_tab=active_tab,    
                           followers=followers_count, 
                           following=following_count, 
                           is_following=is_following)

# 3. Fitur Follow
@user_bp.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    
    if not user_to_follow:
        flash('User tidak ditemukan.', 'danger')
        return redirect(url_for('frontend.home'))
    
    if user_to_follow == current_user:
        flash('Kamu tidak bisa follow diri sendiri!', 'warning')
        return redirect(url_for('user.profile', username=username))

    if not current_user.is_following(user_to_follow):
        current_user.follow(user_to_follow)
        
        # Buat Notifikasi
        notif = Notification(user_id=user_to_follow.id, actor_id=current_user.id, 
                             type='follow', message='mulai mengikuti Anda.')
        db.session.add(notif)
        db.session.commit()
        flash(f'Kamu sekarang mengikuti {username}!', 'success')
        
    return redirect(request.referrer or url_for('user.profile', username=username))

# 4. Fitur Unfollow
@user_bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user_to_unfollow = User.query.filter_by(username=username).first()
    
    if user_to_unfollow:
        current_user.unfollow(user_to_unfollow)
        db.session.commit()
        flash(f'Kamu berhenti mengikuti {username}.', 'info')
        
    return redirect(request.referrer or url_for('user.profile', username=username))

# 5. Edit Profil
@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_username = request.form.get('username')
        new_bio = request.form.get('bio')
        
        # Validasi Username (Cek apakah sudah dipakai orang lain)
        if new_username != current_user.username:
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user:
                flash('Username sudah dipakai orang lain!', 'danger')
                return redirect(url_for('user.edit_profile'))

        # A. Upload Foto Profil
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                current_user.profile_pic = filename

        # B. Upload Foto Sampul
        if 'cover_pic' in request.files:
            file = request.files['cover_pic']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filename = 'cover_' + filename 
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                current_user.cover_pic = filename

        # Simpan Data Teks
        current_user.name = new_name
        current_user.username = new_username
        current_user.bio = new_bio
        
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('user.profile', username=current_user.username))

    # Render template edit profil (pastikan file html-nya ada)
    return render_template('main/profile_edit.html')