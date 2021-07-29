from flask import Flask, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
# from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")
    
    app.secret_key = '!secret'
    app.config.from_object('config')

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth = OAuth(app)
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    @app.route('/')
    def homepage():
        user = session.get('user')
        return render_template('home.html', user=user)
    
    @app.route('/login')
    def login():
        redirect_uri = url_for('auth', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)

    @app.route('/auth')
    def auth():
        token = oauth.google.authorize_access_token()
        user = oauth.google.parse_id_token(token)
        session['user'] = user
        if user["email_verified"]:
            user_id = user["sub"]
            user_email = user["email"]
            picture = user["picture"]
            user_name = user["given_name"]
        else:
            return "User email not available or not verified by Google.", 400
        current_user = Author.query.filter_by(email=user_email).all()
        if not current_user:
            new_author = Author(username=user_name, email=user_email, avatar=picture)
            db.session.add(new_author)
            db.session.commit()
        return redirect('/')


    @app.route('/logout')
    def logout():
        session.pop('user', None)
        return redirect('/')

    
    from app.models.author import Author
    from app.models.question import Question
    from app.models.answer import Answer
    from app.models.question_vote import Question_Vote
    from app.models.answer_vote import Answer_Vote
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import questions_bp
    
    app.register_blueprint(questions_bp)
    
    
    # CORS(app)
    return app