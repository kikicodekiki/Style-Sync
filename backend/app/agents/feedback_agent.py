"""
Feedback Agent (FA)

Captures user's explicit preference ("Liked" or "Disliked") for outfits
and transforms them into training data points for the Styling Recommendation Agent.

Responsible for:
- Creating JSON training signal files in the feedback_data directory
- Triggering incremental learning in the SRA
- Tracking color/style combinations that users approve or reject
"""

import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class FeedbackAgent:
    """
    PEAS Framework:
    - Performance: Maximize the number of "liked" outfits and saved outfits per user over time
    - Environment: History of outfit recommendations and user reactions
    - Actuators: Creates training signal JSON files, updates preference database
    - Sensors: User feedback signal (boolean/rating), received from API call
    """

    def __init__(self, app_config):
        self.config = app_config
        self.feedback_dir = app_config.get('FEEDBACK_DATA_DIR', 'feedback_data')
        os.makedirs(self.feedback_dir, exist_ok=True)

    def process_feedback(self, user_id, outfit, reaction):
        """
        Process user feedback and create training signal.

        Args:
            user_id: str - the user's ID
            outfit: Outfit model instance
            reaction: str - 'liked' or 'disliked'

        Returns:
            dict - the training signal data
        """
        training_signal = self._extract_training_signal(user_id, outfit, reaction)

        # Write JSON training signal file (triggers incremental learning)
        self._write_training_signal_file(training_signal)

        logger.info(f"Feedback Agent processed {reaction} feedback for outfit {outfit.id}")
        return training_signal

    def _extract_training_signal(self, user_id, outfit, reaction):
        """Extract structured training data from outfit feedback."""
        top = outfit.top_item
        bottom = outfit.bottom_item

        training_signal = {
            'user_id': user_id,
            'outfit_id': outfit.id,
            'reaction': reaction,
            'timestamp': datetime.now().isoformat(),
            'occasion': outfit.occasion,
            'color_combination': {
                'top_colors': top.get_dominant_colors() if top else [],
                'bottom_colors': bottom.get_dominant_colors() if bottom else [],
            },
            'style_combination': {
                'top_style': top.style if top else None,
                'bottom_style': bottom.style if bottom else None,
            },
            'categories': {
                'top_category': top.category if top else None,
                'bottom_category': bottom.category if bottom else None,
            },
            'reward': 1 if reaction == 'liked' else -1,
        }
        return training_signal

    def _write_training_signal_file(self, training_signal):
        """Write training signal to JSON file for the SRA incremental training."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"training_signal_{training_signal['user_id']}_{timestamp}.json"
        filepath = os.path.join(self.feedback_dir, filename)

        try:
            with open(filepath, 'w') as f:
                json.dump(training_signal, f, indent=2)
            logger.info(f"Training signal written to {filepath}")
        except Exception as e:
            logger.error(f"Failed to write training signal: {e}")

    def get_user_preferences(self, user_id):
        """
        Aggregate user preferences from historical feedback for the SRA.
        Scans training signal files to build preference profile.

        Returns:
            dict with liked/disliked color and style combinations
        """
        liked_combinations = []
        disliked_combinations = []

        try:
            for filename in os.listdir(self.feedback_dir):
                if not filename.startswith(f"training_signal_{user_id}"):
                    continue
                filepath = os.path.join(self.feedback_dir, filename)
                with open(filepath, 'r') as f:
                    signal = json.load(f)

                combo = {
                    'top_style': signal['style_combination'].get('top_style'),
                    'bottom_style': signal['style_combination'].get('bottom_style'),
                    'top_colors': signal['color_combination'].get('top_colors', []),
                    'bottom_colors': signal['color_combination'].get('bottom_colors', []),
                    'occasion': signal.get('occasion'),
                }

                if signal['reaction'] == 'liked':
                    liked_combinations.append(combo)
                else:
                    disliked_combinations.append(combo)
        except Exception as e:
            logger.error(f"Failed to aggregate preferences: {e}")

        return {
            'liked_combinations': liked_combinations,
            'disliked_combinations': disliked_combinations,
        }
