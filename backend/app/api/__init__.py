from flask import Blueprint

# Import and register all blueprints
from .auth import auth_bp
from .wardrobe import wardrobe_bp
from .outfit import outfit_bp
from .feedback import feedback_bp
from .weather import weather_bp

__all__ = ['auth_bp', 'wardrobe_bp', 'outfit_bp', 'feedback_bp', 'weather_bp']
