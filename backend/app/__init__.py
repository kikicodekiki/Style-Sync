"""Flask application factory."""

import os
from flask import Flask, send_from_directory
from app.config import config
from app.extensions import db, jwt, cors


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    # Ensure instance and upload folders exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['FEEDBACK_DATA_DIR'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {"origins": "*"},
        r"/uploads/*": {"origins": "*"}
    })

    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.wardrobe import wardrobe_bp
    from app.api.outfit import outfit_bp
    from app.api.feedback import feedback_bp
    from app.api.weather import weather_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(wardrobe_bp)
    app.register_blueprint(outfit_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(weather_bp)

    # Serve uploaded images
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'StyleSync API'}, 200

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
