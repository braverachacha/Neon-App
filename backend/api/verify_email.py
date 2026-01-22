from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

from .models import User
from . import db 

email_app = Blueprint('email_app', __name__)

@email_app.route('/verify-email', methods=['POST'])
def verify_email():
    response = request.get_json()
    
    token_id = response.get('token_id')
    token =response.get('token')
    
    if not token_id or not token:
      return jsonify({'msg':'Missing verification credentials!'}), 400
    user = User.query.filter_by(email_token_id=token_id).first()
    
    if not user or not user.check_email_token(token):
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