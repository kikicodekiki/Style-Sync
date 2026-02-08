"""Feedback service - processes user feedback and triggers RL training."""

import json
import logging
from flask import current_app
from app.extensions import db
from app.models.feedback import Feedback, TrainingSignal
from app.models.outfit import Outfit
from app.agents.feedback_agent import FeedbackAgent

logger = logging.getLogger(__name__)


class FeedbackService:

    @staticmethod
    def submit_feedback(user_id, outfit_id, reaction):
        """
        Submit user feedback for an outfit.

        Delegates to Feedback Agent which:
        1. Creates a Feedback record
        2. Extracts training signal
        3. Writes JSON training file for SRA incremental training
        """
        outfit = Outfit.query.filter_by(id=outfit_id, user_id=user_id).first()
        if not outfit:
            return None, "Outfit not found"

        # Store feedback in database
        feedback = Feedback(
            user_id=user_id,
            outfit_id=outfit_id,
            reaction=reaction,
        )
        db.session.add(feedback)

        # Delegate to Feedback Agent for training signal creation
        fa = FeedbackAgent(current_app.config)
        training_signal = fa.process_feedback(user_id, outfit, reaction)

        # Store training signal in database
        top = outfit.top_item
        bottom = outfit.bottom_item
        ts = TrainingSignal(
            user_id=user_id,
            outfit_id=outfit_id,
            reaction=reaction,
            color_combination=json.dumps({
                'top_colors': top.get_dominant_colors() if top else [],
                'bottom_colors': bottom.get_dominant_colors() if bottom else [],
            }),
            style_combination=f"{top.style if top else 'unknown'}+{bottom.style if bottom else 'unknown'}",
            occasion=outfit.occasion,
        )
        db.session.add(ts)
        db.session.commit()

        logger.info(f"Feedback processed: {reaction} for outfit {outfit_id}")
        return feedback.to_dict(), None
