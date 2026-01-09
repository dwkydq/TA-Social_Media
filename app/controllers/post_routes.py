from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Post, PostLike, Comment, Notification, User
import os
import re

post_bp = Blueprint('post', __name__)

# --- 1: Cek User yang Di-mention ---
def get_invalid_users(text):
    if not text: return []
    # Regex menangkap username setelah @ (termasuk titik/underscore)
    usernames = re.findall(r'@([a-zA-Z0-9_.]+)', text)
    usernames = set(usernames)
    
    invalid_users = []
    for username in usernames:
        # Cari user di database
        user = User.query.filter_by(username=username).first()
        if not user:
            invalid_users.append(username)
            
    return invalid_users

# --- HELPER 2: Kirim Notifikasi Mention ---
def process_mentions(text, post_id, type='mention'):
    usernames = re.findall(r'@([a-zA-Z0-9_.]+)', text)
    usernames = set(usernames)

    for username in usernames:
        user = User.query.filter_by(username=username).first()
        if user and user != current_user:
            # Cek notifikasi duplikat
            existing_notif = Notification.query.filter_by(
                user_id=user.id, 
                actor_id=current_user.id, 
                type='mention', 
                post_id=post_id
            ).first()

            if not existing_notif:
                msg = 'menandai Anda dalam sebuah postingan.' if type == 'post' else 'menyebut Anda dalam komentar.'
                notif = Notification(
                    user_id=user.id, 
                    actor_id=current_user.id, 
                    type='mention', 
                    post_id=post_id, 
                    message=msg
                )
                db.session.add(notif)
    db.session.commit()

# --- 1. BUAT POSTINGAN ---
@post_bp.route('/post/create', methods=['POST'])
@login_required
def create_post():
    caption = request.form.get('caption', '').strip()
    media_filename = None
    
    # 1. Cek Media
    if 'media' in request.files:
        file = request.files['media']
        if file.filename != '':
            media_filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], media_filename))
    
    # 2. Validasi Input Kosong
    if not caption and not media_filename:
        flash('Postingan tidak boleh kosong!', 'danger')
        return redirect(url_for('frontend.home'))

    # 3. VALIDASI MENTION
    invalid_users = get_invalid_users(caption)
    if invalid_users:
        # Jika ada user yang tidak valid, batalkan posting
        flash(f'User tidak ditemukan: {", ".join(["@" + u for u in invalid_users])}', 'danger')
        if media_filename:
            try:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], media_filename))
            except:
                pass
        return redirect(url_for('frontend.home'))

    # 4. Simpan Postingan (Jika lolos validasi)
    new_post = Post(user_id=current_user.id, caption=caption, media_url=media_filename)
    db.session.add(new_post)
    db.session.commit()
    
    # 5. Kirim Notif Mention
    if caption:
        process_mentions(caption, new_post.id, type='post')
    
    flash('Berhasil memposting!', 'success')
    return redirect(url_for('frontend.home'))

# --- 2. HAPUS POSTINGAN ---
@post_bp.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('Anda tidak berhak menghapus postingan ini.', 'danger')
        return redirect(url_for('frontend.home'))
    
    if post.media_url:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], post.media_url))
        except:
            pass 

    db.session.delete(post)
    db.session.commit()
    flash('Postingan dihapus.', 'info')
    return redirect(url_for('frontend.home'))

# --- 3. FITUR LIKE ---
@post_bp.route('/post/<int:post_id>/like')
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
    else:
        new_like = PostLike(user_id=current_user.id, post_id=post.id)
        db.session.add(new_like)
        if post.author != current_user:
            notif = Notification(user_id=post.author.id, actor_id=current_user.id, 
                                 type='like', post_id=post.id, message='menyukai postingan Anda.')
            db.session.add(notif)
        db.session.commit()
    
    return redirect(request.referrer or url_for('frontend.home'))

# --- 4. DETAIL POST ---
@post_bp.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('main/post_detail.html', post=post)

# --- 5. TAMBAH KOMENTAR ---
@post_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content', '').strip()

    if not content:
        flash('Komentar tidak boleh kosong.', 'warning')
        return redirect(request.referrer or url_for('frontend.home'))

    # VALIDASI MENTION DI KOMENTAR
    invalid_users = get_invalid_users(content)
    if invalid_users:
        flash(f'Komentar gagal: User {", ".join(["@" + u for u in invalid_users])} tidak ditemukan.', 'danger')
        return redirect(request.referrer or url_for('frontend.home'))

    # Simpan Komentar
    comment = Comment(user_id=current_user.id, post_id=post.id, content=content)
    db.session.add(comment)
    
    # Notifikasi Komen Biasa
    if post.author != current_user:
        notif = Notification(user_id=post.author.id, actor_id=current_user.id, 
                             type='comment', post_id=post.id, message=f'mengomentari: {content[:20]}...')
        db.session.add(notif)
        
    db.session.commit()

    # Kirim Notif Mention
    process_mentions(content, post.id, type='comment')

    return redirect(request.referrer or url_for('frontend.home'))

# --- 6. HAPUS KOMENTAR ---
@post_bp.route('/comment/<int:comment_id>/delete')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user and comment.post.author != current_user:
        flash('Tidak ada izin hapus komentar.', 'danger')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Komentar dihapus.', 'info')
        
    return redirect(url_for('post.post_detail', post_id=comment.post_id))