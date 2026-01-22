from flask import Blueprint, jsonify, request, current_app

from .models import User
from . import db 
from .utils import generate_email_token, send_email_verification, send_password_reset_email

from .password_check import check_password

forgot = Blueprint('forgot', __name__)

@forgot.route('/forgot-password', methods=['POST'])  
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'msg':'Email not found'}), 404
    
    token = generate_email_token()
    expiry_time = datetime.utcnow() + timedelta(minutes=15)
    
    user.set_reset_token(token) # hash the token
    user.reset_token_expiry = expiry_time
    user.reset_token_used = False
    db.session.commit()
    
    frontend_url = current_app.config['FRONTEND_LINK'].strip('/')
    reset_link = f"{frontend_url}/forgot-password.html?token={token}"
    send_password_reset_email(email, reset_link)
    return jsonify({'msg': 'Password reset link sent to your email'}), 200