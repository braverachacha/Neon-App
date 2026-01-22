from flask import Blueprint
from flask_jwt_extended import jwt_required

protect = Blueprint('protect', __name__)


@protect.route('/protected-route', methods=['GET'])
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    return jsonify({
        'msg': 'Access granted',
        'user': current_user
    }), 200