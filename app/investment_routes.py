from flask import Blueprint, request, jsonify
from app.extensions import mongo  # ✅ no longer import from app/__init__.py

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
