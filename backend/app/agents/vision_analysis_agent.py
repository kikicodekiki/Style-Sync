"""
Vision Analysis Agent (VAA)

Processes uploaded clothing images using:
- YOLOv8 for object detection (category identification)
- ColorThief for dominant color extraction
- OpenCV and Pillow for image preprocessing
- LLaMA via Ollama for intelligent style classification

Transforms raw image data into structured clothing metadata.
"""

import os
import json
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

# Optional heavy dependencies with graceful fallback
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("Pillow not available - image preprocessing disabled")

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logger.warning("OpenCV not available - advanced preprocessing disabled")

try:
    from colorthief import ColorThief
    COLORTHIEF_AVAILABLE = True
except ImportError:
    COLORTHIEF_AVAILABLE = False
    logger.warning("ColorThief not available - color extraction disabled")

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logger.warning("Ultralytics YOLO not available - object detection disabled")


# Clothing categories YOLOv8 can map to our domain
YOLO_TO_CLOTHING_MAP = {
    'shirt': 'shirt',
    't-shirt': 'shirt',
    'top': 'top',
    'blouse': 'blouse',
    'hoodie': 'hoodie',
    'sweater': 'hoodie',
    'jacket': 'jacket',
    'coat': 'jacket',
    'pants': 'pants',
    'trousers': 'pants',
    'jeans': 'jeans',
    'skirt': 'skirt',
    'dress': 'dress',
    'shorts': 'pants',
    'leggings': 'pants',
}

TOP_CATEGORIES = {'shirt', 'top', 'blouse', 'hoodie', 'jacket', 'dress'}
BOTTOM_CATEGORIES = {'pants', 'jeans', 'skirt', 'leggings'}


class VisionAnalysisAgent:
    """
    PEAS Framework:
    - Performance: Accuracy of clothing detection and classification (type, color, style)
    - Environment: Uploaded clothing images from users
    - Actuators: Structured clothing metadata stored in wardrobe database
    - Sensors: Uploaded images, YOLOv8 detection, ColorThief color data, OpenCV/Pillow preprocessing
    """

    def __init__(self, app_config):
        self.config = app_config
        self._yolo_model = None
        self.ollama_url = app_config.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.ollama_model = app_config.get('OLLAMA_MODEL', 'llama3.2')

    def _get_yolo_model(self):
        """Lazy-load YOLOv8 model."""
        if not YOLO_AVAILABLE:
            return None
        if self._yolo_model is None:
            try:
                # Use nano model for speed; it handles general object detection
                self._yolo_model = YOLO('yolov8n.pt')
                logger.info("YOLOv8 model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load YOLOv8 model: {e}")
                return None
        return self._yolo_model

    def analyze_image(self, image_path, user_metadata=None):
        """
        Main entry point: analyze an uploaded clothing image.

        Args:
            image_path: Path to the saved image file
            user_metadata: Optional dict with user-provided overrides
                          (category, style, weather_suitability)

        Returns:
            dict with: category, style, weather_suitability, outfit_part,
                       dominant_colors, detected_by_ai
        """
        result = {
            'category': None,
            'style': None,
            'weather_suitability': None,
            'outfit_part': None,
            'dominant_colors': [],
            'detected_by_ai': False,
        }

        # Step 1: Preprocess image
        preprocessed_path = self._preprocess_image(image_path)

        # Step 2: Extract dominant colors
        result['dominant_colors'] = self._extract_colors(preprocessed_path or image_path)

        # Step 3: Detect clothing category via YOLOv8
        detected_category = self._detect_category_yolo(preprocessed_path or image_path)

        # Step 4: Use LLaMA for style classification if category detected
        if detected_category:
            result['category'] = detected_category
            result['detected_by_ai'] = True
            ai_classification = self._classify_with_llama(
                image_path, detected_category, result['dominant_colors']
            )
            result.update(ai_classification)

        # Step 5: Apply user overrides (user metadata takes precedence)
        if user_metadata:
            for key in ['category', 'style', 'weather_suitability']:
                if user_metadata.get(key):
                    result[key] = user_metadata[key]
                    if key == 'category':
                        result['detected_by_ai'] = False

        # Step 6: Infer outfit_part from category if not set
        if result['category'] and not result.get('outfit_part'):
            result['outfit_part'] = self._infer_outfit_part(result['category'])

        # Ensure required fields have defaults
        result['category'] = result['category'] or 'shirt'
        result['style'] = result['style'] or 'casual'
        result['weather_suitability'] = result['weather_suitability'] or 'warm'
        result['outfit_part'] = result['outfit_part'] or 'top'

        return result

    def _preprocess_image(self, image_path):
        """Preprocess image using OpenCV and Pillow for better analysis."""
        if not PIL_AVAILABLE:
            return None
        try:
            img = Image.open(image_path)

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize to standard size for consistent processing
            img = img.resize((640, 640), Image.Resampling.LANCZOS)

            preprocessed_path = image_path + '_preprocessed.jpg'
            img.save(preprocessed_path, 'JPEG', quality=95)
            return preprocessed_path
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            return None

    def _extract_colors(self, image_path):
        """Extract dominant colors from clothing image using ColorThief."""
        if not COLORTHIEF_AVAILABLE:
            return self._extract_colors_pillow(image_path)

        try:
            ct = ColorThief(image_path)
            palette = ct.get_palette(color_count=3, quality=10)
            hex_colors = [self._rgb_to_hex(rgb) for rgb in palette]
            logger.info(f"Extracted colors: {hex_colors}")
            return hex_colors
        except Exception as e:
            logger.error(f"ColorThief extraction failed: {e}")
            return self._extract_colors_pillow(image_path)

    def _extract_colors_pillow(self, image_path):
        """Fallback color extraction using Pillow."""
        if not PIL_AVAILABLE:
            return []
        try:
            img = Image.open(image_path).convert('RGB')
            img = img.resize((100, 100))
            pixels = list(img.getdata())
            # Simple dominant color: average of most common pixels
            r = sum(p[0] for p in pixels) // len(pixels)
            g = sum(p[1] for p in pixels) // len(pixels)
            b = sum(p[2] for p in pixels) // len(pixels)
            return [self._rgb_to_hex((r, g, b))]
        except Exception as e:
            logger.error(f"Pillow color extraction failed: {e}")
            return []

    def _detect_category_yolo(self, image_path):
        """Use YOLOv8 to detect clothing category in the image."""
        model = self._get_yolo_model()
        if not model:
            return None

        try:
            results = model(image_path, verbose=False)
            for result in results:
                for box in result.boxes:
                    class_name = model.names[int(box.cls[0])].lower()
                    if class_name in YOLO_TO_CLOTHING_MAP:
                        mapped = YOLO_TO_CLOTHING_MAP[class_name]
                        logger.info(f"YOLOv8 detected: {class_name} -> {mapped}")
                        return mapped
            return None
        except Exception as e:
            logger.error(f"YOLOv8 detection failed: {e}")
            return None

    def _classify_with_llama(self, image_path, detected_category, colors):
        """Use LLaMA via Ollama to classify style and weather suitability."""
        try:
            import requests
            color_str = ', '.join(colors) if colors else 'unknown'
            prompt = f"""You are a fashion expert. A clothing item has been detected as a '{detected_category}'
with dominant colors: {color_str}.

Based on this information, classify the clothing item:
1. Style: Choose ONE from [casual, formal, sporty]
2. Weather suitability: Choose ONE from [warm, cold]

Respond ONLY with a JSON object in this exact format:
{{"style": "<style>", "weather_suitability": "<weather>"}}"""

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                text = data.get('response', '{}')
                try:
                    classification = json.loads(text)
                    return {
                        'style': classification.get('style', 'casual'),
                        'weather_suitability': classification.get('weather_suitability', 'warm'),
                    }
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.warning(f"LLaMA classification failed (Ollama may not be running): {e}")

        return {'style': 'casual', 'weather_suitability': 'warm'}

    def _infer_outfit_part(self, category):
        """Infer whether clothing is a top or bottom based on category."""
        if category in TOP_CATEGORIES:
            return 'top'
        elif category in BOTTOM_CATEGORIES:
            return 'bottom'
        return 'top'

    @staticmethod
    def _rgb_to_hex(rgb):
        """Convert RGB tuple to hex color string."""
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
