from flask import jsonify
import re

def check_password(password):
    # 1. Length Check
    if len(password) < 8:
        return jsonify({'msg': 'Password should be at least 8 characters!'}), 400
  
  # For upper or lower case
    if not re.search(r'[a-zA-Z]', password):
        return jsonify({'msg': 'Password must contain at least one letter (capital or small)! balances'}), 400
    
    # for num or special character
    if not re.search(r'[0-9!@#$%^&*(),.?":{}|<>]', password):
        return jsonify({'msg': 'Password must contain at least one number or special character!'}), 400
        
    return jsonify({'msg': 'Password Verified and accepted'}), 200