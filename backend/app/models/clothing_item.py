import uuid
import json
from datetime import datetime
from app.extensions import db


class ClothingItem(db.Model):
    __tablename__ = 'clothing_items'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

    # Classification attributes
    category = db.Column(db.String(50), nullable=False)  # shirt, top, blouse, hoodie, pants, jeans, skirt
    style = db.Column(db.String(50), nullable=False)     # casual, formal, sporty
    weather_suitability = db.Column(db.String(20), nullable=False)  # cold, warm
    outfit_part = db.Column(db.String(10), nullable=True)  # top, bottom

    # AI-extracted metadata
    dominant_colors = db.Column(db.Text, nullable=True)  # JSON array of hex colors
    detected_by_ai = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_dominant_colors(self):
        if self.dominant_colors:
            try:
                return json.loads(self.dominant_colors)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def set_dominant_colors(self, colors):
        self.dominant_colors = json.dumps(colors)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_url': self.image_url,
            'category': self.category,
            'style': self.style,
            'weather': self.weather_suitability,
            'outfit_part': self.outfit_part,
            'dominant_colors': self.get_dominant_colors(),
            'detected_by_ai': self.detected_by_ai,
            'created_at': self.created_at.isoformat(),
        }
