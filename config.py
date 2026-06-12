import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    """Base Configuration - جميع الإعدادات الأساسية"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://localhost/instagram_repost'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 20)),
    }
    
    # Redis & Cache
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    )
    
    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'UTC'
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
    
    # Encryption
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'default-key-32-chars-exactly')
    
    # Instagram
    INSTAGRAM_RATE_LIMIT = int(os.getenv('INSTAGRAM_RATE_LIMIT', 5))
    INSTAGRAM_TIMEOUT = int(os.getenv('INSTAGRAM_TIMEOUT', 30))
    INSTAGRAM_MAX_VIDEOS = int(os.getenv('INSTAGRAM_MAX_VIDEOS', 10))
    INSTAGRAM_SESSION_FILE = 'instagram_session.json'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Security
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Features
    ENABLE_EMAIL_VERIFICATION = os.getenv('ENABLE_EMAIL_VERIFICATION', 'True').lower() == 'true'
    ENABLE_TWO_FACTOR_AUTH = os.getenv('ENABLE_TWO_FACTOR_AUTH', 'False').lower() == 'true'
    ENABLE_API_DOCS = os.getenv('ENABLE_API_DOCS', 'True').lower() == 'true'
    
    # Email
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SMTP_FROM = os.getenv('SMTP_FROM', 'noreply@example.com')

class DevelopmentConfig(BaseConfig):
    """Development Configuration - إعدادات التطوير"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False

class ProductionConfig(BaseConfig):
    """Production Configuration - إعدادات الإنتاج"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    # Add more strict security settings
    
class TestingConfig(BaseConfig):
    """Testing Configuration - إعدادات الاختبار"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
