from flask import Blueprint, jsonify, request, url_for, current_app, send_from_directory
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from datetime import datetime, timedelta
import secrets

import requests


from .models import User
from . import db 

from .utils import generate_email_token, send_email_verification, send_password_reset_email

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
  
  user = User.query.filter_by(email=email).first()
  if user:
    return jsonify({'msg':'Email already exists!'}), 400
  else:
    new_user = User(
      username=username,
      email=email,
      )
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    token = generate_email_token(new_user.email)
    frontend_url = current_app.config['FRONTEND_LINK']
    link = f"{frontend_url}/verify.html?token={token}"
        
    send_email_verification(new_user.email, link, new_user.username)
    return jsonify({'msg':'Account created successfully! Please check your email to verify your account.'}), 201


@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'msg': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    # Create a token valid for 5 minutes (300 sec)
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt='password-reset')

    # Store token in DB for single-use
    user.reset_token = token
    db.session.commit()

    reset_link = f"{FRONTEND_LINK}/reset.html?token={token}"

    # Send email
    msg = Message(
        subject="NeonApp Password Reset",
        recipients=[email],
        body=f"Reset your password using this link (expires in 5 minutes): {reset_link}"
    )
    mail.send(msg)

    return jsonify({'msg': 'Reset link sent! Check your email.'}), 200

# Reset password
@auth.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')

    if not token or not new_password:
        return jsonify({'msg': 'Missing token or password'}), 400

    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        # Verify token is valid and not older than 5 minutes
        email = serializer.loads(token, salt='password-reset', max_age=300)
    except SignatureExpired:
        return jsonify({'msg': 'Reset link expired', 'error': 'expired'}), 400
    except BadSignature:
        return jsonify({'msg': 'Invalid reset link', 'error': 'invalid'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'msg': 'User not found', 'error': 'invalid'}), 404

    # Check token matches stored token
    if user.reset_token != token:
        return jsonify({'msg': 'Reset link already used or invalid', 'error': 'invalid'}), 400

    # Update password and invalidate token
    user.set_password(new_password)
    user.reset_token = None
    db.session.commit()

    return jsonify({'msg': 'Password reset successful! Redirecting to login...'}), 200
  
  


@auth.route('/verify-email/<token>')
def verify_email(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=900)
    except SignatureExpired:
        return jsonify({'success': False, 'msg': 'Token expired', 'error': 'expired'}), 400
    except BadSignature:
        return jsonify({'success': False, 'msg': 'Invalid token', 'error': 'invalid'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'success': False, 'msg': 'User not found', 'error': 'invalid'}), 404

    if not user.is_verified:
        user.is_verified = True
        db.session.commit()
        return jsonify({'success': True, 'msg': 'Email verified successfully'}), 200
    
    return jsonify({'success': True, 'msg': 'Email already verified'}), 200
    

@auth.route('/protected-route', methods=['GET'])
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    return jsonify({
        'msg': 'Access granted',
        'user': current_user
    }), 200