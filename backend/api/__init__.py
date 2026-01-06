from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from flask_mail import Mail
import os


db = SQLAlchemy()
mail = Mail()

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['FRONTEND_LINK'] = os.getenv('FRONTEND_LINK')
    
    # JWT CONFIGURATION
    
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 18000 # 30 MIN
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400 # 1 DAY
    
    # FLASK MAIL SETUP
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    
    db.init_app(app)
    JWTManager(app)
    mail.init_app(app)
    
    from .auth import auth
    
    app.register_blueprint(auth, url_prefix='')

    return app