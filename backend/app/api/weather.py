"""Weather API controller - fetches and returns current weather data."""

import logging
import requests
from flask import Blueprint, jsonify, current_app

weather_bp = Blueprint('weather', __name__)
logger = logging.getLogger(__name__)


@weather_bp.route('/api/weather', methods=['GET'])
def get_weather():
    """
    Retrieve current weather from OpenWeatherMap API.
    Falls back to mock data if API key is not configured.
    """
    api_key = current_app.config.get('OPENWEATHER_API_KEY', '')
    city = current_app.config.get('OPENWEATHER_CITY', 'Sofia')

    if not api_key:
        # Return mock weather data for development
        return jsonify(_mock_weather(city)), 200

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather = {
            'temperature': data['main']['temp'],
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'city': data['name'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
        }
        return jsonify(weather), 200

    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API request failed: {e}")
        return jsonify(_mock_weather(city)), 200
    except (KeyError, ValueError) as e:
        logger.error(f"Weather API response parsing failed: {e}")
        return jsonify(_mock_weather(city)), 200


def _mock_weather(city):
    """Return mock weather data for development/fallback."""
    return {
        'temperature': 18,
        'condition': 'Clear',
        'description': 'clear sky',
        'city': city,
        'humidity': 60,
        'wind_speed': 5.5,
    }
