from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db, socketio
from app.models import User, Message
from flask_socketio import emit

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
@login_required
def chat_list():
    # --- LOGIKA MUTUAL FOLLOW (Saling Follow) ---
    
    following_list = current_user.following.all()
    following_ids = {f.followed_id for f in following_list}

    followers_list = current_user.followers.all()
    follower_ids = {f.follower_id for f in followers_list}

    mutual_ids = following_ids.intersection(follower_ids)

    if mutual_ids:
        users = User.query.filter(User.id.in_(mutual_ids)).all()
    else:
        users = []
    
    return render_template('chat/chat_list.html', users=users)

# 2. HALAMAN ROOM CHAT (Isi percakapan dengan seseorang)
@chat_bp.route('/chat/<username>')
@login_required
def chat_room(username):
    recipient = User.query.filter_by(username=username).first_or_404()
    
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == recipient.id)) |
        ((Message.sender_id == recipient.id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return render_template('chat/chat_room.html', recipient=recipient, messages=messages)

# 3. WEBSOCKET EVENT (Kirim Pesan Realtime)
@socketio.on('send_message')
def handle_send_message_event(data):
    recipient_username = data['recipient']
    body = data['message']
    
    recipient = User.query.filter_by(username=recipient_username).first()
    
    if recipient:
        # Simpan ke Database
        msg = Message(sender_id=current_user.id, recipient_id=recipient.id, body=body)
        db.session.add(msg)
        db.session.commit()
        
        emit('receive_message', {
            'body': body,
            'sender': current_user.username,
            'recipient': recipient.username,
            'avatar': current_user.profile_pic,
            'time': msg.timestamp.strftime('%H:%M')
        }, broadcast=True)