from flask import Flask
from .routes import user_bp
from .db import init_db

def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(user_bp)
    return app