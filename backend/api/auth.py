from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jwt_identity
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from datetime import datetime, timedelta
import secrets
from urllib.parse import quote

from .models import User
from . import db 
from .utils import generate_email_token, send_email_verification, send_password_reset_email

from .password_check import check_password

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    response = request.get_json()
    
    email = response.get('email')
    password = response.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        if not user.is_verified:
            return jsonify({'msg': 'Please check your email to verify your account!'}), 403
        access_token = create_access_token(identity=user.email, fresh=True)
        refresh_token = create_refresh_token(identity=user.email)
        return jsonify({
            'msg':'Logged in successfully!',
            'access_token':access_token,
            'refresh_token':refresh_token,
        }), 200
    else:
        return jsonify({'msg':'Invalid username or password'}), 401

@auth.route('/register', methods=['POST'])
def register():
    response = request.get_json()
    
    username = response.get('username')
    email = response.get('email')
    password = response.get('password')
    

    # SERVER SIDE VALIDATION
    if len(username) < 2:
        return jsonify({'msg':'Username should be greater than 2 characters!'}), 400
    if len(email) < 2 or '@' not in email or '.' not in email:
        return jsonify({'msg':'Enter a valid email!'}), 400
        
    password_response= check_password(password)
    if password_response[1] == 400:
      return password_response
    
    # CHECK IF USER EXISTS
    if User.query.filter_by(email=email).first():
        return jsonify({'msg':'Email already exists!'}), 409
        
    # GENERATE TOKEN & TOKEN ID
    token = generate_email_token()
    token_id = secrets.token_urlsafe(8)
    expiry_time = datetime.utcnow() + timedelta(minutes=15)
    

    # CREATE USER OBJECT
    new_user = User(
        username=username,
        email=email,
        email_token_id=token_id,
        email_token_expiry=expiry_time
    )
    
    new_user.set_password(password)
    new_user.set_email_token(token)
    

    # BUILD EMAIL VERIFICATION LINK

    frontend_url = current_app.config['FRONTEND_LINK'].strip('/')
    link = f"{frontend_url}/verify-email?token_id={token_id}&token={token}"
    
    if not send_email_verification(email, link, username):
      return {"message": "Failed to send verification email"}, 500
      
    # SAVE USER AFTER EMAIL SUCCESS
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'msg':'Account created successfully! Please check your email to verify your account.'}), 201

@auth.route('/forgot-password', methods=['POST'])  
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

@auth.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'msg':'Missing token or password'}), 400
    elif len(new_password) < 8:
      return jsonify({'msg': 'Password should be greater than 8 characters!'}), 400
    
    # Find user by reset token
    user = User.query.filter_by(reset_token=token).first()
    
    if not user:
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

@auth.route('/verify-email/<token_id>/<token>')
def verify_email(token):
    user = User.query.filter_by(token_id=email_token_id).first()
    
    if not user:
        return jsonify({'success': False, 'msg': 'Invalid token', 'error': 'invalid'}), 400
    
    # Check if token expired
    if user.email_token_expiry < datetime.utcnow():
        return jsonify({'success': False, 'msg': 'Token expired', 'error': 'expired'}), 400
    
    # Check if already verified
    if user.is_verified:
        return jsonify({'success': True, 'msg': 'Email already verified'}), 200
    
    # Mark as verified and clear token
    user.is_verified = True
    user.email_token = None
    user.email_token_expiry = None
    db.session.commit()
    
    return jsonify({'success': True, 'msg': 'Email verified successfully'}), 200

@auth.route('/protected-route', methods=['GET'])
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    return jsonify({
        'msg': 'Access granted',
        'user': current_user
    }), 200