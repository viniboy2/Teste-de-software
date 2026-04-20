from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import login_usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response, status = login_usuario(data)
    return jsonify(response), status
