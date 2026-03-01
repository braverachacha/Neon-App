import secrets
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

from ..models import User
from ..utils import send_email_verification, generate_email_token

from ..extensions import db

resend_link_bp = Blueprint('resend_link', __name__)

@resend_link_bp.route('/resend-link', methods=['POST'])
def resend_link():
    request_data = request.get_json()

    token_id = request_data.get('token_id')

    if not token_id:
        return jsonify{'msg': 'Invalid request'}, 400

    user = User.query.filter_by(email_token_id=token_id).first()

    if user:
        username = user.username
        email = user.email
        
        # new token and token_id for the email verification link
        token = generate_email_token()
        token_id = secrets.token_urlsafe(8)

        frontend_url = current_app.config['FRONTEND_URL'].rstrip('/')

        link = f"{frontend_url}/verify.html?token_id={token_id}&token={token}"

        user.set_email_token(token) # hash the token 
        user.email_token_id = token_id
        user.email_token_expiry = datetime.utcnow() + timedelta(minutes=15) # 15 minutes
        user.is_verified = False

        db.session.commit()

        # send the email verification link to the user
        send_email_verification(email, username, link)

    return jsonify({'msg': 'If the user exists, the email verification link have been sent successfully.'}), 200
    
