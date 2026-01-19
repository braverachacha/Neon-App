from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(550), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Email verification fields
    email_token = db.Column(db.String(300), nullable=True)
    email_token_expiry = db.Column(db.DateTime, nullable=True)
    
    # Password reset fields  
    reset_token = db.Column(db.String(300), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    reset_token_used = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)