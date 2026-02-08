"""Outfit service - coordinates the SRA agent for outfit generation and management."""

import json
import logging
from flask import current_app
from app.extensions import db
from app.models.clothing_item import ClothingItem
from app.models.outfit import Outfit, SavedOutfit
from app.agents.styling_recommendation_agent import StylingRecommendationAgent
from app.agents.feedback_agent import FeedbackAgent

logger = logging.getLogger(__name__)


class OutfitService:

    @staticmethod
    def generate_outfit(user_id, occasion, weather_data):
        """
        Generate an AI-powered outfit recommendation.

        Coordinates:
        1. Fetch wardrobe items from database
        2. Retrieve user preferences from Feedback Agent
        3. Invoke SRA to generate recommendation
        4. Persist the generated outfit
        """
        # Fetch user's wardrobe
        wardrobe_items = ClothingItem.query.filter_by(user_id=user_id).all()
        if not wardrobe_items:
            return None, "Your wardrobe is empty. Add some clothing items first!"

        # Get user preferences from feedback history
        fa = FeedbackAgent(current_app.config)
        user_preferences = fa.get_user_preferences(user_id)

        # Invoke SRA
        sra = StylingRecommendationAgent(current_app.config)
        recommendation = sra.generate_outfit(
            wardrobe_items, occasion, weather_data, user_preferences
        )

        if not recommendation:
            return None, "Could not generate an outfit. Please add more items to your wardrobe."

        # Persist the outfit
        top = recommendation.get('top')
        bottom = recommendation.get('bottom')

        outfit = Outfit(
            user_id=user_id,
            top_item_id=top.id if top else None,
            bottom_item_id=bottom.id if bottom else None,
            occasion=occasion,
            weather_data=json.dumps(weather_data),
            explanation=recommendation.get('explanation', ''),
        )
        db.session.add(outfit)
        db.session.commit()

        return outfit.to_dict(), None

    @staticmethod
    def get_saved_outfits(user_id):
        """Get all saved outfits for a user."""
        saved = SavedOutfit.query.filter_by(user_id=user_id).order_by(
            SavedOutfit.saved_at.desc()
        ).all()
        return [s.to_dict() for s in saved]

    @staticmethod
    def save_outfit(user_id, outfit_id):
        """Save an outfit to favorites."""
        outfit = Outfit.query.filter_by(id=outfit_id, user_id=user_id).first()
        if not outfit:
            return False, "Outfit not found"

        # Check if already saved
        existing = SavedOutfit.query.filter_by(user_id=user_id, outfit_id=outfit_id).first()
        if existing:
            return True, None  # Already saved, no error

        saved = SavedOutfit(user_id=user_id, outfit_id=outfit_id)
        db.session.add(saved)
        db.session.commit()
        return True, None

    @staticmethod
    def get_outfit(outfit_id, user_id):
        """Get a specific outfit."""
        outfit = Outfit.query.filter_by(id=outfit_id, user_id=user_id).first()
        return outfit
