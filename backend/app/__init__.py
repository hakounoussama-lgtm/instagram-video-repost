from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery
from redis import Redis
import logging
import os
from datetime import datetime

# Initialize Extensions
db = SQLAlchemy()
jwt = JWTManager()
celery = Celery(__name__)
redis_client = None

def create_app(config_name='development'):
    """Application Factory - إنشاء تطبيق Flask"""
    
    from config import config
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize Redis
    global redis_client
    redis_client = Redis.from_url(app.config['REDIS_URL'], decode_responses=True)
    
    # Initialize Celery
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    
    # Setup Logging
    setup_logging(app)
    
    # Register Blueprints
    register_blueprints(app)
    
    # Register Error Handlers
    register_error_handlers(app)
    
    # Register CLI Commands
    register_cli_commands(app)
    
    # Create Database Tables
    with app.app_context():
        db.create_all()
    
    return app

def register_blueprints(app):
    """Register Flask Blueprints - تسجيل المسارات"""
    
    from app.routes import auth_bp, repost_bp, user_bp, stats_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(repost_bp, url_prefix='/api/repost')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')

def register_error_handlers(app):
    """Register Error Handlers - معالجات الأخطاء"""
    
    from app.utils.exceptions import APIException, ValidationError
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = {
            'success': False,
            'error': error.message,
            'code': error.code
        }
        return response, error.status_code
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = {
            'success': False,
            'error': 'Validation Error',
            'details': error.details
        }
        return response, 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return {
            'success': False,
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }, 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        return {
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }, 500

def register_cli_commands(app):
    """Register CLI Commands - أوامر سطر الأوامر"""
    
    @app.cli.command()
    def init_db():
        """Initialize the database - تهيئة قاعدة البيانات"""
        db.create_all()
        print('Database initialized!')
    
    @app.cli.command()
    def seed_db():
        """Seed the database - ملء قاعدة البيانات ببيانات تجريبية"""
        # Implementation here
        print('Database seeded!')

def setup_logging(app):
    """Setup Logging Configuration - إعداد نظام التسجيل"""
    
    import logging
    from logging.handlers import RotatingFileHandler
    from pythonjsonlogger import jsonlogger
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # File Handler with JSON formatter
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(
        jsonlogger.JsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
    )
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(app.config['LOG_LEVEL'])
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
