from flask import Blueprint, jsonify
from datetime import datetime

alive = Blueprint('alive', __name__) 

@alive.route('/ping')
def ping():
    return jsonify({
        'status': 'alive',
        'msg': 'NeonApp backend is running',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'neonapp-api',
        'version': '1.0.0'
    })