from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(550), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Email verification fields
    email_token_id = db.Column(db.String(16), index=True)
    email_token = db.Column(db.String(300), nullable=True)
    email_token_expiry = db.Column(db.DateTime, nullable=True)
    
    # Password reset fields 
    reset_token_id = db.Column(db.String(16), index=True)
    reset_token = db.Column(db.String(300), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    reset_token_used = db.Column(db.Boolean, default=False)
    
    # PASSWORD HASHING
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    # EMAIL TOKEN HASHING
    def set_email_token(self, email_token):
        self.email_token = generate_password_hash(email_token)
        
    def check_email_token(self, email_token):
      if not email_token or not self.email_token:
        return False
      return check_password_hash(self.email_token, email_token)
        
    # RESET TOKEN HASHING
    def set_reset_token(self, reset_token):
      self.reset_token = generate_password_hash(reset_token)
      
    def check_reset_token(self, reset_token):
      if not reset_token:
        return False
      return check_password_hash(self.reset_token, reset_token)