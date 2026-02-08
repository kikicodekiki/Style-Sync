"""
Styling Recommendation Agent (SRA)

Generates context-aware outfit recommendations based on:
- Occasion (casual, gym, formal, friends, work)
- Weather conditions (via Weather API data)
- User preferences (learned from feedback history)
- Wardrobe metadata (style/weather suitability labels)

Uses LLaMA via Ollama for intelligent outfit pairing and explanation.
Undergoes incremental learning triggered by the Feedback Agent.
"""

import json
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)


# Occasion-to-style mapping for rule-based fallback
OCCASION_STYLE_MAP = {
    'gym': ['sporty'],
    'friends': ['casual', 'sporty'],
    'formal': ['formal'],
    'casual': ['casual', 'sporty'],
    'work': ['formal', 'casual'],
}

# Weather temperature thresholds
WARM_THRESHOLD = 15  # degrees Celsius


class StylingRecommendationAgent:
    """
    PEAS Framework:
    - Performance: User satisfaction with outfit suggestions, contextual relevance (weather, occasion)
    - Environment: Virtual wardrobe data, user preferences, contextual information
    - Actuators: Personalized outfit recommendations with explanations; updated recommendation history
    - Sensors: Weather API data, wardrobe metadata, user preferences
    """

    def __init__(self, app_config):
        self.config = app_config
        self.ollama_url = app_config.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.ollama_model = app_config.get('OLLAMA_MODEL', 'llama3.2')

    def generate_outfit(self, wardrobe_items, occasion, weather_data, user_preferences=None):
        """
        Generate an outfit recommendation.

        Args:
            wardrobe_items: List of ClothingItem model instances
            occasion: str - the occasion for the outfit
            weather_data: dict - current weather information
            user_preferences: dict - learned preferences from feedback history

        Returns:
            dict with: top_item, bottom_item, explanation
        """
        if not wardrobe_items:
            return None

        # Step 1: Filter items by weather suitability
        weather_suitable = self._filter_by_weather(wardrobe_items, weather_data)

        # Step 2: Filter by occasion style
        occasion_suitable = self._filter_by_occasion(weather_suitable, occasion)

        # Step 3: Separate tops and bottoms
        tops = [item for item in occasion_suitable if item.outfit_part == 'top' or
                item.category in {'shirt', 'top', 'blouse', 'hoodie', 'jacket', 'dress'}]
        bottoms = [item for item in occasion_suitable if item.outfit_part == 'bottom' or
                   item.category in {'pants', 'jeans', 'skirt', 'leggings'}]

        # Fallback: use all items if filtered lists are too small
        if not tops:
            tops = [item for item in wardrobe_items if item.outfit_part == 'top' or
                    item.category in {'shirt', 'top', 'blouse', 'hoodie', 'jacket', 'dress'}]
        if not bottoms:
            bottoms = [item for item in wardrobe_items if item.outfit_part == 'bottom' or
                       item.category in {'pants', 'jeans', 'skirt', 'leggings'}]

        if not tops or not bottoms:
            return self._single_item_outfit(wardrobe_items, occasion, weather_data)

        # Step 4: Score and select best combination using preferences
        top, bottom = self._select_best_pair(tops, bottoms, user_preferences, occasion)

        # Step 5: Generate explanation with LLaMA
        explanation = self._generate_explanation(top, bottom, occasion, weather_data)

        return {
            'top': top,
            'bottom': bottom,
            'explanation': explanation,
        }

    def _filter_by_weather(self, items, weather_data):
        """Filter clothing items by weather suitability."""
        temp = weather_data.get('temperature', weather_data.get('temp', 20))
        is_warm = temp >= WARM_THRESHOLD

        suitable = []
        for item in items:
            if is_warm and item.weather_suitability == 'warm':
                suitable.append(item)
            elif not is_warm and item.weather_suitability == 'cold':
                suitable.append(item)
            elif item.weather_suitability not in ('warm', 'cold'):
                suitable.append(item)  # Include items with no specific suitability

        return suitable if suitable else items  # Fallback to all items

    def _filter_by_occasion(self, items, occasion):
        """Filter clothing items by occasion-appropriate styles."""
        preferred_styles = OCCASION_STYLE_MAP.get(occasion, ['casual'])

        suitable = [item for item in items if item.style in preferred_styles]
        return suitable if suitable else items  # Fallback to all items

    def _select_best_pair(self, tops, bottoms, user_preferences, occasion):
        """Select the best top-bottom combination based on preferences."""
        if not user_preferences:
            return random.choice(tops), random.choice(bottoms)

        # Score pairs based on liked color combinations and styles
        liked_combinations = user_preferences.get('liked_combinations', [])
        best_score = -1
        best_top = random.choice(tops)
        best_bottom = random.choice(bottoms)

        for top in tops:
            for bottom in bottoms:
                score = self._score_combination(top, bottom, liked_combinations, occasion)
                if score > best_score:
                    best_score = score
                    best_top = top
                    best_bottom = bottom

        return best_top, best_bottom

    def _score_combination(self, top, bottom, liked_combinations, occasion):
        """Score a top-bottom combination based on learned preferences."""
        score = 0

        for liked in liked_combinations:
            # Reward matching style combinations
            if (liked.get('top_style') == top.style and
                    liked.get('bottom_style') == bottom.style):
                score += 2

            # Reward matching color combinations
            top_colors = top.get_dominant_colors()
            bottom_colors = bottom.get_dominant_colors()
            liked_top_colors = liked.get('top_colors', [])
            liked_bottom_colors = liked.get('bottom_colors', [])

            for tc in top_colors:
                if tc in liked_top_colors:
                    score += 1
            for bc in bottom_colors:
                if bc in liked_bottom_colors:
                    score += 1

        return score

    def _single_item_outfit(self, wardrobe_items, occasion, weather_data):
        """Handle case where only tops or bottoms exist."""
        item = random.choice(wardrobe_items)
        explanation = self._generate_explanation(
            item if item.outfit_part == 'top' else None,
            item if item.outfit_part == 'bottom' else None,
            occasion,
            weather_data,
        )
        return {
            'top': item if item.outfit_part == 'top' else None,
            'bottom': item if item.outfit_part == 'bottom' else None,
            'explanation': explanation,
        }

    def _generate_explanation(self, top, bottom, occasion, weather_data):
        """Use LLaMA via Ollama to generate a natural language outfit explanation."""
        top_desc = self._describe_item(top) if top else "no top selected"
        bottom_desc = self._describe_item(bottom) if bottom else "no bottom selected"
        temp = weather_data.get('temperature', weather_data.get('temp', 20))
        condition = weather_data.get('condition', weather_data.get('weather', 'clear'))

        try:
            import requests
            prompt = f"""You are a professional fashion stylist. Create a brief, encouraging outfit recommendation explanation.

Outfit details:
- Top: {top_desc}
- Bottom: {bottom_desc}
- Occasion: {occasion}
- Weather: {condition}, {temp}°C

Write 2-3 sentences explaining why this outfit works for the occasion and weather. Be specific about color coordination and style. Keep it friendly and concise."""

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60,
            )

            if response.status_code == 200:
                data = response.json()
                explanation = data.get('response', '').strip()
                if explanation:
                    logger.info("LLaMA generated outfit explanation successfully")
                    return explanation
        except Exception as e:
            logger.warning(f"LLaMA explanation failed (Ollama may not be running): {e}")

        # Fallback: rule-based explanation
        return self._fallback_explanation(top, bottom, occasion, weather_data)

    def _describe_item(self, item):
        """Create a text description of a clothing item."""
        if not item:
            return "none"
        colors = ', '.join(item.get_dominant_colors()[:2]) if item.get_dominant_colors() else "unknown color"
        return f"{colors} {item.style} {item.category}"

    def _fallback_explanation(self, top, bottom, occasion, weather_data):
        """Generate a simple rule-based explanation when LLaMA is unavailable."""
        temp = weather_data.get('temperature', weather_data.get('temp', 20))
        condition = weather_data.get('condition', weather_data.get('weather', 'clear'))

        parts = []
        if top:
            parts.append(f"a {top.style} {top.category}")
        if bottom:
            parts.append(f"{bottom.style} {bottom.category}")

        outfit_str = " paired with ".join(parts) if parts else "this outfit"
        temp_desc = "warm" if temp >= WARM_THRESHOLD else "cold"

        return (f"This outfit combines {outfit_str}, perfect for a {occasion} occasion. "
                f"With {condition} weather at {temp}°C, this {temp_desc}-weather "
                f"ensemble keeps you stylish and comfortable.")
