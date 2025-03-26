from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from app import mongo


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Investment Plan structure
investment_plan_schema = {
    "plan_name": str,
    "amount": float,
    "duration_months": int,
    "expected_return": float,
    "risk_level": str,
    "description": str,
}

def user_schema(user):
    return {
        "username": user["username"],
        "role": user.get("role", "user")
    }
