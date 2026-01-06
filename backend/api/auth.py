from flask import Blueprint, jsonify, request, url_for, current_app, send_from_directory
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

import requests


from .models import User
from . import db 

from .utils import generate_email_token, send_email_verification

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
        
    send_email_verification(new_user.email, link)
    return jsonify({'msg':'Account created successfully! Please check your email to verify your account.'}), 201


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