from flask import Blueprint, jsonify, request, current_app
from .utils import generate_email_token
from .password_check import check_password
from datetime import datetime, timedelta
import secrets

from .models import User

from .utils import generate_email_token, send_email_verification, send_password_reset_email

from . import db

reg = Blueprint('reg', __name__) 

@reg.route('/register', methods=['POST'])
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
    link = f"{frontend_url}/verify.html?token_id={token_id}&token={token}"
    
    if not send_email_verification(email, link, username):
      return {"message": "Failed to send verification email"}, 500
      
    # SAVE USER AFTER EMAIL SUCCESS
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'msg':'Account created successfully! Please check your email to verify your account.'}), 201