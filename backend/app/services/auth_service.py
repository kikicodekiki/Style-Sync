"""Authentication service - business logic for login/signup."""

import bcrypt
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User


class AuthService:

    @staticmethod
    def signup(username, password):
        """Register a new user."""
        if User.query.filter_by(username=username).first():
            return None, "Username already exists"

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id)
        return {'token': token, 'userId': user.id, 'username': user.username}, None

    @staticmethod
    def login(username, password):
        """Authenticate a user."""
        user = User.query.filter_by(username=username).first()
        if not user:
            return None, "Invalid username or password"

        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return None, "Invalid username or password"

        token = create_access_token(identity=user.id)
        return {'token': token, 'userId': user.id, 'username': user.username}, None

    @staticmethod
    def get_user(user_id):
        """Get user by ID."""
        return User.query.get(user_id)
