from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from .models import User

login = Blueprint('login', __name__) 

@login.route('/login', methods=['POST'])
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