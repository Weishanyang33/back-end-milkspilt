from flask import Flask, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
from google.oauth2 import id_token
from google.auth.transport import requests
import time
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")
    
    app.config.update(
        DEBUG=True,
        SECRET_KEY=os.environ.get("GOOGLE_CLIENT_SECRET"),
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
    )

    
    from app.models.author import Author
    from app.models.question import Question
    from app.models.answer import Answer
    from app.models.question_vote import Question_Vote
    from app.models.answer_vote import Answer_Vote
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import questions_bp
    from .routes import answers_bp
    from .routes import login_bp
    from .routes import authors_bp
    
    app.register_blueprint(questions_bp)
    app.register_blueprint(answers_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(authors_bp)
    
    
    CORS(app)
    return app