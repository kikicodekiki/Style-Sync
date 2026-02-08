"""Wardrobe service - manages clothing items CRUD and delegates to VAA."""

import os
import uuid
import logging
from werkzeug.utils import secure_filename
from flask import current_app
from app.extensions import db
from app.models.clothing_item import ClothingItem
from app.agents.vision_analysis_agent import VisionAnalysisAgent

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class WardrobeService:

    @staticmethod
    def get_wardrobe(user_id):
        """Get all clothing items for a user."""
        items = ClothingItem.query.filter_by(user_id=user_id).order_by(
            ClothingItem.created_at.desc()
        ).all()
        return [item.to_dict() for item in items]

    @staticmethod
    def add_item(user_id, file, form_data):
        """
        Add a new clothing item with image analysis via VAA.

        Args:
            user_id: str
            file: uploaded file object
            form_data: dict with category, style, weather_suitability
        """
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        # Save uploaded image
        filename = None
        image_url = None
        image_path = None

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4()}.{ext}"
            filename = secure_filename(unique_name)
            image_path = os.path.join(upload_folder, filename)
            file.save(image_path)
            image_url = f"/uploads/{filename}"

        # Use VAA to analyze the image
        user_metadata = {
            'category': form_data.get('category'),
            'style': form_data.get('style'),
            'weather_suitability': form_data.get('weather') or form_data.get('weather_suitability'),
        }

        if image_path:
            try:
                vaa = VisionAnalysisAgent(current_app.config)
                analysis = vaa.analyze_image(image_path, user_metadata)
            except Exception as e:
                logger.error(f"VAA analysis failed: {e}")
                analysis = user_metadata
                analysis['dominant_colors'] = []
                analysis['detected_by_ai'] = False
        else:
            analysis = user_metadata
            analysis['dominant_colors'] = []
            analysis['detected_by_ai'] = False

        # Ensure required fields
        category = analysis.get('category') or 'shirt'
        style = analysis.get('style') or 'casual'
        weather = analysis.get('weather_suitability') or 'warm'
        outfit_part = analysis.get('outfit_part') or form_data.get('outfit_part') or 'top'

        item = ClothingItem(
            user_id=user_id,
            filename=filename,
            image_url=image_url,
            category=category,
            style=style,
            weather_suitability=weather,
            outfit_part=outfit_part,
            detected_by_ai=analysis.get('detected_by_ai', False),
        )
        item.set_dominant_colors(analysis.get('dominant_colors', []))

        db.session.add(item)
        db.session.commit()

        return item.to_dict()

    @staticmethod
    def get_item(user_id, item_id):
        """Get a specific clothing item."""
        item = ClothingItem.query.filter_by(id=item_id, user_id=user_id).first()
        return item.to_dict() if item else None

    @staticmethod
    def delete_item(user_id, item_id):
        """Delete a clothing item and its image file."""
        item = ClothingItem.query.filter_by(id=item_id, user_id=user_id).first()
        if not item:
            return False, "Item not found"

        # Remove image file
        if item.filename:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            image_path = os.path.join(upload_folder, item.filename)
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    logger.warning(f"Could not delete image file: {e}")

        db.session.delete(item)
        db.session.commit()
        return True, None
