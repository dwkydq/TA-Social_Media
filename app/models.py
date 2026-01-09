from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- TABEL FOLLOWS ---
class Follow(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- TABEL USERS ---
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    profile_pic = db.Column(db.String(255))
    cover_pic = db.Column(db.String(255))
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    likes = db.relationship('PostLike', backref='user', lazy=True)
    
    # Relasi Followers/Following
    following = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref='follower', lazy='dynamic')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref='followed', lazy='dynamic')

    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(f)

    def unfollow(self, user):
        f = self.following.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

# --- TABEL POSTS ---
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    caption = db.Column(db.Text)
    media_url = db.Column(db.String(255))
    media_type = db.Column(db.Enum('text', 'image', 'video'), default='text')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relasi ke Comment & Like
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('PostLike', backref='post', lazy=True, cascade="all, delete-orphan")

    def is_liked_by(self, user):
        return PostLike.query.filter_by(user_id=user.id, post_id=self.id).first() is not None

# --- TABEL COMMENTS ---
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- TABEL LIKES ---
class PostLike(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- TABEL NOTIFICATIONS ---
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Penerima notif
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Pelaku (yg like/komen)
    type = db.Column(db.Enum('like', 'comment', 'follow', 'message', 'mention'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relasi untuk ambil info Actor (Pelaku)
    actor = db.relationship('User', foreign_keys=[actor_id], lazy=True)

# --- TABEL CHATS ---
class Message(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')