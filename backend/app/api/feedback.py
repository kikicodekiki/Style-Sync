"""Feedback API controller - handles user outfit feedback."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.feedback_service import FeedbackService

feedback_bp = Blueprint('feedback', __name__)


def _verify_user(user_id):
    current_user = get_jwt_identity()
    return current_user == user_id


@feedback_bp.route('/api/users/<user_id>/feedback', methods=['POST'])
@jwt_required()
def submit_feedback(user_id):
    if not _verify_user(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Request body is required'}), 400

    outfit_id = data.get('outfit_id')
    reaction = data.get('feedback') or data.get('reaction')

    if not outfit_id or not reaction:
        return jsonify({'message': 'outfit_id and feedback are required'}), 400

    if reaction not in ('liked', 'disliked'):
        return jsonify({'message': 'feedback must be "liked" or "disliked"'}), 400

    result, error = FeedbackService.submit_feedback(user_id, outfit_id, reaction)
    if error:
        return jsonify({'message': error}), 404

    return jsonify({'message': 'Feedback submitted successfully', 'feedback': result}), 200
