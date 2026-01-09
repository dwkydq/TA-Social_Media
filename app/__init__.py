from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from .config import Config
import re
from markupsafe import Markup

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Silakan login untuk mengakses halaman ini."
    login_manager.login_message_category = "warning"

    # --- FILTER KHUSUS UNTUK MENTION LINK ---
    @app.template_filter('linkify_mentions')
    def linkify_mentions(text):
        if not text: return ""
        pattern = r'@([a-zA-Z0-9_.]+)'
        replacement = r'<a href="/\1" class="text-xyz-yellow font-bold hover:underline">@\1</a>'
        return Markup(re.sub(pattern, replacement, text))

    # --- REGISTER BLUEPRINTS ---
    from .controllers.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from .controllers.post_routes import post_bp
    app.register_blueprint(post_bp)

    from .controllers.frontend_routes import frontend_bp
    app.register_blueprint(frontend_bp)

    from .controllers.user_routes import user_bp
    app.register_blueprint(user_bp)

    from app.controllers import chat_routes
    app.register_blueprint(chat_routes.chat_bp)

    return app