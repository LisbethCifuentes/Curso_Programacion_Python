from flask import Flask
from dotenv import load_dotenv
import os
from .db import init_db
from .routes.pets_routes import pets_bp
from .routes.auth_routes import auth_bp

def create_app():
    load_dotenv()  # lee .env

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")

    # inicializar DB
    init_db(app)

    # registrar blueprints
    app.register_blueprint(pets_bp, url_prefix="/pets")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def home():
        return "API de Mascotas con MongoDB y SSR funcionando"

    return app
