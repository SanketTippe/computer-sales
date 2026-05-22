import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sanket-computers-secret-key-2024'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'bwoc0wbiohcd7lulo3iv-mysql.services.clever-cloud.com'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'urkj6e4vd5nlvhpp'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'YOUR_PASSWORD_HERE'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'bwoc0wbiohcd7lulo3iv'
    SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Upload Settings
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Pagination
    PRODUCTS_PER_PAGE = 12
    REVIEWS_PER_PAGE = 10

    # Cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Payment Configuration
UPI_ID = "sankettippe9766@oksbi"
RAZORPAY_KEY_ID = ""
RAZORPAY_KEY_SECRET = ""

# Site Settings
SITE_NAME = "Sanket's Computers & Sales"
SITE_EMAIL = "sankettippe9766@gmail.com"
SITE_PHONE = "+91 9766575428"
FREE_SHIPPING_THRESHOLD = 1000
SHIPPING_CHARGE = 100
TAX_RATE = 18
LOYALTY_POINTS_RATIO = 10  # Rs 10 = 1 point