from flask import Blueprint, jsonify, request
from datetime import datetime

from .models import User
from . import db 
from .utils import generate_email_token, send_email_verification, send_password_reset_email

from .password_check import check_password

pass_reset = Blueprint('pass_reset', __name__)

@pass_reset.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    
    token_id = data.get('token_id')
    token = data.get('token')
    new_password = data.get('password')
    
    print(f"""
    Token id : {token_id} \n 
    Reset token {token} \n
    """)
    
    if not token or not token_id or not new_password:
        return jsonify({'msg':'Missing token or password'}), 400
    elif len(new_password) < 8:
      return jsonify({'msg': 'Password should be greater than 8 characters!'}), 400
    # ADD PASSWORD STRENGTH ENFORCEMENT
    
    # Find user by reset token
    user = User.query.filter_by(reset_token_id=token_id).first()
    
    if not user or not user.check_reset_token(token):
        return jsonify({'msg':'Invalid reset link', 'error':'invalid'}), 400
    
    # Check if token expired
    if user.reset_token_expiry < datetime.utcnow():
        return jsonify({'msg':'Reset link expired', 'error':'expired'}), 400
    
    # Check if token already used
    if user.reset_token_used:
        return jsonify({'msg':'Reset link already used', 'error':'used'}), 400
    
    # Update password and mark token as used
    user.set_password(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    user.reset_token_used = True
    db.session.commit()
    
    return jsonify({'msg':'Password reset successful! Redirecting to login...'}), 200