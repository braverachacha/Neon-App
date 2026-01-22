from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from flask_mail import Mail

from sqlalchemy_utils import database_exists, create_database

import os

db = SQLAlchemy()
mail = Mail()

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    frontend_url = os.getenv('FRONTEND_LINK')
    
    if not frontend_url:
      raise RuntimeError('FRONTEND_LINK is missing in your environment variables!')
      
    CORS(
      app,
      origins=[frontend_url],
      supports_credentials=True
      )
    
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
    
    from .alive import alive
    from .register import reg
    from .protected_route import protect
    from .forgot_password import forgot
    from .login import login_bp
    from .reset_password import pass_reset
    from .verify_email import email_app
    
    app.register_blueprint(alive)
    app.register_blueprint(reg)
    app.register_blueprint(protect)
    app.register_blueprint(forgot)
    app.register_blueprint(login_bp)
    app.register_blueprint(pass_reset)
    app.register_blueprint(email_app)
    
    init_db(app)

    return app
    
def init_db(app):
    """Create MySQL database + tables once if not existing"""
    with app.app_context():
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
        db.create_all()