"""Authentication API controller - handles login and signup endpoints."""

from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    result, error = AuthService.login(data['username'], data['password'])
    if error:
        return jsonify({'message': error}), 401

    return jsonify(result), 200


@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    if len(data['password']) < 6:
        return jsonify({'message': 'Password must be at least 6 characters'}), 400

    result, error = AuthService.signup(data['username'], data['password'])
    if error:
        return jsonify({'message': error}), 409

    return jsonify(result), 201


@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    # JWT is stateless; client removes token
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = AuthService.get_user(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict()), 200
