import uuid
import json
from datetime import datetime
from app.extensions import db


class Outfit(db.Model):
    __tablename__ = 'outfits'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    top_item_id = db.Column(db.String(36), db.ForeignKey('clothing_items.id'), nullable=True)
    bottom_item_id = db.Column(db.String(36), db.ForeignKey('clothing_items.id'), nullable=True)

    occasion = db.Column(db.String(50), nullable=True)
    weather_data = db.Column(db.Text, nullable=True)  # JSON snapshot of weather at generation time
    explanation = db.Column(db.Text, nullable=True)   # LLaMA-generated explanation

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    top_item = db.relationship('ClothingItem', foreign_keys=[top_item_id])
    bottom_item = db.relationship('ClothingItem', foreign_keys=[bottom_item_id])
    saved_records = db.relationship('SavedOutfit', backref='outfit', lazy=True, cascade='all, delete-orphan')

    def get_weather_data(self):
        if self.weather_data:
            try:
                return json.loads(self.weather_data)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'outfit_id': self.id,
            'user_id': self.user_id,
            'top': self.top_item.to_dict() if self.top_item else None,
            'bottom': self.bottom_item.to_dict() if self.bottom_item else None,
            'occasion': self.occasion,
            'weather': self.get_weather_data(),
            'explanation': self.explanation,
            'created_at': self.created_at.isoformat(),
        }


class SavedOutfit(db.Model):
    __tablename__ = 'saved_outfits'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    outfit_id = db.Column(db.String(36), db.ForeignKey('outfits.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        outfit_data = self.outfit.to_dict() if self.outfit else {}
        outfit_data['saved_at'] = self.saved_at.isoformat()
        return outfit_data
