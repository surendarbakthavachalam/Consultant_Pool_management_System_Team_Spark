# project/__init__.py
from flask import Flask
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a-very-secure-and-unique-secret-key-for-your-hackathon'
    
    # --- MongoDB Connection ---
    MONGO_CONNECTION_STRING = "mongodb+srv://user:12345@cluster1.qjxgsoy.mongodb.net/"
    client = MongoClient(MONGO_CONNECTION_STRING)
    app.db = client.pool_management_system

    from .auth import auth_bp
    from .admin import admin_bp
    from .consultant import consultant_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(consultant_bp)

    return app