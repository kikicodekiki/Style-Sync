import uuid
from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    wardrobe_items = db.relationship('ClothingItem', backref='owner', lazy=True, cascade='all, delete-orphan')
    outfits = db.relationship('Outfit', backref='owner', lazy=True, cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'userId': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
        }
