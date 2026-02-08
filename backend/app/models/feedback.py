import uuid
import json
from datetime import datetime
from app.extensions import db


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    outfit_id = db.Column(db.String(36), db.ForeignKey('outfits.id'), nullable=False)
    reaction = db.Column(db.String(10), nullable=False)  # 'liked' or 'disliked'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    outfit = db.relationship('Outfit', backref='feedbacks')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'outfit_id': self.outfit_id,
            'reaction': self.reaction,
            'timestamp': self.timestamp.isoformat(),
        }


class TrainingSignal(db.Model):
    """Stores reinforcement learning training signals from user feedback."""
    __tablename__ = 'training_signals'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    outfit_id = db.Column(db.String(36), db.ForeignKey('outfits.id'), nullable=False)
    reaction = db.Column(db.String(10), nullable=False)
    color_combination = db.Column(db.Text, nullable=True)  # JSON of top+bottom colors
    style_combination = db.Column(db.String(100), nullable=True)  # e.g. "casual+casual"
    occasion = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_color_combination(self):
        if self.color_combination:
            try:
                return json.loads(self.color_combination)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'outfit_id': self.outfit_id,
            'reaction': self.reaction,
            'color_combination': self.get_color_combination(),
            'style_combination': self.style_combination,
            'occasion': self.occasion,
            'created_at': self.created_at.isoformat(),
        }
