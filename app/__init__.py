from flask import Flask
from flask_jwt_extended import JWTManager
from .extensions import mongo  # ✅ Use shared instance
from .investment_routes import investment  # ✅ Blueprint

jwt = JWTManager()  # ✅ Initialize JWT here

def create_app():
    app = Flask(__name__)

    # ✅ MongoDB Config
    app.config["MONGO_URI"] = "mongodb://localhost:27017/finbee_db"

    # ✅ JWT Config
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]

    # ✅ Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)

    # ✅ Register blueprints
    from .routes import main
    from .auth_routes import auth
    from .investment_routes import investment

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(investment, url_prefix="/investment")

    return app
