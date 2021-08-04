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
    
    # app.secret_key = '!secret'
    # app.config.from_object('config')

    # CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    # oauth = OAuth(app)
    # oauth.register(
    #     name='google',
    #     server_metadata_url=CONF_URL,
    #     client_kwargs={
    #         'scope': 'openid email profile'
    #     }
    # )
    
    # @app.route('/')
    # def homepage():
    #     user = session.get('user')
    #     return render_template('home.html', user=user)
    
    # @app.route('/login')
    # def login():
    #     redirect_url = url_for('auth', _external=True)
    #     return oauth.google.authorize_redirect(redirect_url)
    

    # @app.route('/auth')
    # def auth():
        # token = oauth.google.authorize_access_token()["id_token"]
        # token = oauth.google.parse_id_token(t)
        # print(token)
        
        # token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjBmY2MwMTRmMjI5MzRlNDc0ODBkYWYxMDdhMzQwYzIyYmQyNjJiNmMiLCJ0eXAiOiJKV1QifQeyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDI2NTM1NzY2MTU3LWlnMXRxZnJzNjBnMm1wNmpyYjJkNmh0cW9xdDQzOGw5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTAyNjUzNTc2NjE1Ny1pZzF0cWZyczYwZzJtcDZqcmIyZDZodHFvcXQ0MzhsOS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExODQ0NTkwMTA0OTgyMTM5OTQ2NyIsImVtYWlsIjoid2Vpc2hhbnlhbmczM0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IjQ2RmwxVjVLck9rUGhfT0Q0WnlVY2ciLCJub25jZSI6IklvTGY5ZUFNaFJVVXQ4REVHVFlDIiwibmFtZSI6IldlaXNoYW4gWWFuZyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp3eGJDeExHQWJTS0tKd0VPSVNZTjZXeEVFUGNOX1NHdGRUYjV6OT1zOTYtYyIsImdpdmVuX25hbWUiOiJXZWlzaGFuIiwiZmFtaWx5X25hbWUiOiJZYW5nIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2Mjc5NjMyNzYsImV4cCI6MTYyNzk2Njg3Nn0u2EuzMwNlZS1EIVc2ejVp-Ur3YMPFVnTbE5fcUJ6cibWhCUnvbMqC_3_RSO-CoN0o_kj7eG6skmUrZxs2qKrNmb1ciazWh2W9Bk3W_mApevH9BRMN68NhQqZGgMG2IvQ6-O1V8jzQuNeUEiipbrH6kIloqsecT-J9eKHjBVUUOIOGGkt0jk-mUw_pyISbfjiug2sOl-kJ50n_2_R5Qj1E3wip9V0m9RsvrGtgRbuGHilByJQEHi_-m23DI0cLNuNQvz1437vyAxG1TYmPt14X5JoOvZXGxzghmzQH_TtXVxniSrD071sjTtN6_EUBhZocsN5cNh49sDMfntQpjGM3w'
        # print(token)
        # time.sleep(60)
        # print('heloooooo')
        # request = requests.Request()
        # id_info = id_token.verify_oauth2_token(token, request, '1026535766157-ig1tqfrs60g2mp6jrb2d6htqoqt438l9.apps.googleusercontent.com')
        # userid = id_info['sub']
        # print('~~~~~')
        # print(id_info)
        # print(userid)
        # session['user'] = user
        # if user["email_verified"]:
        #     user_id = user["sub"]
        #     user_email = user["email"]
        #     picture = user["picture"]
        #     user_name = user["given_name"]
        # else:
        #     return "User email not available or not verified by Google.", 400
        # current_user = Author.query.filter_by(email=user_email).all()
        # if not current_user:
        #     new_author = Author(username=user_name, email=user_email, avatar=picture)
        #     db.session.add(new_author)
        #     db.session.commit()
        # return redirect('/')


    # @app.route('/logout')
    # def logout():
    #     session.pop('user', None)
        # return redirect('/')

    
    from app.models.author import Author
    from app.models.question import Question
    from app.models.answer import Answer
    from app.models.question_vote import Question_Vote
    from app.models.answer_vote import Answer_Vote
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import questions_bp
    from .routes import login_bp
    
    app.register_blueprint(questions_bp)
    app.register_blueprint(login_bp)
    
    
    CORS(app)
    return app