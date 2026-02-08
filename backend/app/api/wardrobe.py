"""Wardrobe API controller - manages clothing items."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.wardrobe_service import WardrobeService

wardrobe_bp = Blueprint('wardrobe', __name__)


def _verify_user(user_id):
    """Check that the requesting user matches the resource owner."""
    current_user = get_jwt_identity()
    return current_user == user_id


@wardrobe_bp.route('/api/users/<user_id>/wardrobe', methods=['GET'])
@jwt_required()
def get_wardrobe(user_id):
    if not _verify_user(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    items = WardrobeService.get_wardrobe(user_id)
    return jsonify(items), 200


@wardrobe_bp.route('/api/users/<user_id>/wardrobe', methods=['POST'])
@jwt_required()
def add_item(user_id):
    if not _verify_user(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    file = request.files.get('image')
    form_data = {
        'category': request.form.get('category', ''),
        'style': request.form.get('style', ''),
        'weather': request.form.get('weather', ''),
        'weather_suitability': request.form.get('weather_suitability', ''),
        'outfit_part': request.form.get('outfit_part', ''),
    }

    if not form_data['category'] or not form_data['style']:
        return jsonify({'message': 'Category and style are required'}), 400

    item = WardrobeService.add_item(user_id, file, form_data)
    return jsonify(item), 201


@wardrobe_bp.route('/api/users/<user_id>/wardrobe/<item_id>', methods=['GET'])
@jwt_required()
def get_item(user_id, item_id):
    if not _verify_user(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    item = WardrobeService.get_item(user_id, item_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404
    return jsonify(item), 200


@wardrobe_bp.route('/api/users/<user_id>/wardrobe/<item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(user_id, item_id):
    if not _verify_user(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    success, error = WardrobeService.delete_item(user_id, item_id)
    if not success:
        return jsonify({'message': error}), 404
    return jsonify({'message': 'Item deleted successfully'}), 200
