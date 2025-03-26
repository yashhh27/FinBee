jwt_blacklist = set()
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for

from app import mongo, jwt

auth = Blueprint("auth", __name__)

# Token revocation logic
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in jwt_blacklist

# Register a new user
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if mongo.db.users.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({
        "username": username,
        "password": hashed_password,
        "role": "user"  # Default role
    })

    return jsonify({"message": "User registered successfully"}), 201

# Login a user
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({"username": data.get("username")})

    if user and check_password_hash(user['password'], data.get("password")):
        access_token = create_access_token(
            identity=user['username'],
            additional_claims={"role": user.get("role", "user")}
        )
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid credentials"}), 401

# Logout a user
@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_blacklist.add(jti)
    return jsonify(message="Successfully logged out"), 200

# Protected test route
@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello, {current_user}! This is a protected route."), 200

# Promote user to admin (admin only)
@auth.route('/promote/<username>', methods=['POST'])
@jwt_required()
def promote_user(username):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify(message="Admins only!"), 403

    result = mongo.db.users.update_one(
        {"username": username},
        {"$set": {"role": "admin"}}
    )

    if result.modified_count == 0:
        return jsonify(message="User not found or already an admin"), 404

    return jsonify(message=f"{username} has been promoted to admin."), 200

@auth.route('/promote', methods=['GET', 'POST'])
@jwt_required()
def promote_ui():
    current_user = get_jwt_identity()
    claims = get_jwt()
    if claims.get("role") != "admin":
        return render_template("promote.html", message="Only admins can promote users.")

    if request.method == "POST":
        username = request.form.get("username")
        result = mongo.db.users.update_one(
            {"username": username},
            {"$set": {"role": "admin"}}
        )
        if result.matched_count == 0:
            return render_template("promote.html", message="User not found.")
        return render_template("promote.html", message=f"User '{username}' promoted to admin.")

    return render_template("promote.html")