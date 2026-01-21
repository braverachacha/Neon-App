from flask import jsonify
import re

def check_password(password):
    if len(password) < 8:
        return jsonify({'msg': 'Password should be more than 8 characters!'}), 400

    if not re.search(r'[a-z]', password):
        return jsonify({'msg': 'Password must contain at least one lowercase letter!'}), 400

    if not re.search(r'[A-Z]', password):
        return jsonify({'msg': 'Password must contain at least one uppercase letter!'}), 400

    if not re.search(r'[0-9]', password):
        return jsonify({'msg': 'Password must contain at least one number!'}), 400

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return jsonify({'msg': 'Password must contain at least one special character!'}), 400
        
    return jsonify({'msg':'Password Verified and accepted'}), 200