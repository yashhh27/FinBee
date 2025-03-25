jwt_blacklist = set()
from flask_jwt_extended import get_jwt

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from app import mongo, jwt


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in jwt_blacklist

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    existing_user = mongo.db.users.find_one({"username": username})
    if existing_user:
        return jsonify(message="Username already exists"), 409

    mongo.db.users.insert_one({"username": username, "password": password})
    return jsonify(message="User registered successfully"), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({"username": data['username']})

    if user and data['password'] == user['password']:
        access_token = create_access_token(identity=user['username'])
        return jsonify(access_token=access_token), 200

    return jsonify(message="Invalid credentials"), 401

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_blacklist.add(jti)
    return jsonify(message="Successfully logged out"), 200


@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello, {current_user}! This is a protected route."), 200