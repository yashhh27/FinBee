from flask import Blueprint, request, jsonify
from app.extensions import mongo  # ✅ no longer import from app/__init__.py
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
investment = Blueprint('investment', __name__)

# Example route
@investment.route('/plans', methods=['GET'])
def get_plans():
    plans = list(mongo.db.investment_plans.find({}, {'_id': 0}))
    return jsonify(plans=plans), 200

@investment.route('/plan', methods=['POST'])
def create_plan():
    data = request.get_json()
    
    required_fields = [
        "plan_name", "amount", "duration_months",
        "expected_return", "risk_level", "description"
    ]

    # ✅ Basic validation
    for field in required_fields:
        if field not in data:
            return jsonify(error=f"Missing field: {field}"), 400

    # ✅ Insert using dict access
    mongo.db["investment_plans"].insert_one(data)

    return jsonify(message="Investment plan created successfully"), 201

@investment.route('/plan/subscribe', methods=['POST'])
@jwt_required()
def subscribe_plan():
    data = request.get_json()
    plan_name = data.get("plan_name")
    amount = data.get("amount")

    if not plan_name or not amount:
        return jsonify(message="Plan name and amount are required"), 400

    # Check if plan exists
    plan = mongo.db.investment_plans.find_one({"plan_name": plan_name})
    if not plan:
        return jsonify(message="Plan not found"), 404

    # Get current user ID from JWT
    user_id = get_jwt_identity()

    # Insert into subscriptions collection
    mongo.db.subscriptions.insert_one({
        "user_id": user_id,
        "plan_name": plan_name,
        "amount": amount,
        "subscribed_on": datetime.utcnow()
    })

    return jsonify(message="Subscribed to investment plan successfully"), 201

@investment.route('/my-plans', methods=['GET'])
@jwt_required()
def get_my_plans():
    user_id = get_jwt_identity()

    subscriptions = list(
        mongo.db.subscriptions.find({"user_id": user_id}, {"_id": 0})
    )

    return jsonify(my_plans=subscriptions), 200
@investment.route('/plan/unsubscribe', methods=['DELETE'])
@jwt_required()
def unsubscribe_plan():
    data = request.get_json()
    plan_name = data.get("plan_name")
    user_id = get_jwt_identity()

    if not plan_name:
        return jsonify(message="Plan name is required"), 400

    result = mongo.db.subscriptions.delete_one({
        "user_id": user_id,
        "plan_name": plan_name
    })

    if result.deleted_count == 0:
        return jsonify(message="Subscription not found"), 404

    return jsonify(message="Unsubscribed from plan successfully"), 200
