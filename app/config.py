"""
Configuration file for the Flask application

* `Config`: Base configuration class
* `DevelopmentConfig`: Configuration for development environment
* `TestingConfig`: Configuration for testing environment
* `ProductionConfig`: Configuration for production environment

"""

import os


class Config:
    DEBUG = os.getenv("DEBUG", False)
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ["json"]

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_ITERATIONS = 10

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
