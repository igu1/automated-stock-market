from flask import Flask
from app.routes.agent_routes import agent_bp
import os

def create_app():
    app = Flask(__name__)
    
    env = os.getenv("FLASK_ENV", "development")
    if env == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    else:
        app.config.from_object("app.config.ProductionConfig")
    app.register_blueprint(agent_bp)
    return app