"""Outfit API controller - handles outfit generation and saved outfits."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.outfit_service import OutfitService

outfit_bp = Blueprint('outfit', __name__)


def _verify_user(user_id):
    current_user = get_jwt_identity()
    return current_user == user_id


@outfit_bp.route('/api/users/<user_id>/outfit/generate', methods=['POST'])
@jwt_required()
def generate_outfit(user_id):
    if not _verify_user(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Request body is required'}), 400

    occasion = data.get('occasion')
    weather_data = data.get('weather', {})

    if not occasion:
        return jsonify({'message': 'Occasion is required'}), 400

    outfit, error = OutfitService.generate_outfit(user_id, occasion, weather_data)
    if error:
        return jsonify({'message': error}), 422

    return jsonify(outfit), 200


@outfit_bp.route('/api/users/<user_id>/outfits/saved', methods=['GET'])
@jwt_required()
def get_saved_outfits(user_id):
    if not _verify_user(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    outfits = OutfitService.get_saved_outfits(user_id)
    return jsonify(outfits), 200


@outfit_bp.route('/api/users/<user_id>/outfits/saved', methods=['POST'])
@jwt_required()
def save_outfit(user_id):
    if not _verify_user(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    outfit_id = data.get('outfit_id') if data else None
    if not outfit_id:
        return jsonify({'message': 'outfit_id is required'}), 400

    success, error = OutfitService.save_outfit(user_id, outfit_id)
    if not success:
        return jsonify({'message': error}), 404

    return jsonify({'message': 'Outfit saved successfully'}), 200
