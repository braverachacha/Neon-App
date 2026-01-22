from flask import Blueprint, jsonify
from datetime import datetime, timedelta

from .models import User
from . import db 

email_app = Blueprint('email_app', __name__)

@email_app.route('/verify-email/<token_id>/<token>')
def verify_email(token_id, token):
    user = User.query.filter_by(email_token_id=token_id).first()
    
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