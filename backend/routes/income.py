from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend import db
from backend.models.income import Income
from . import income_bp

# Create a new income record
@income_bp.route('/add_income', methods=['POST'])
@jwt_required()
def add_income():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Validate required fields
    if not data.get('amount'):
        return jsonify({"message": "Amount is required"}), 400

    # Create a new income record
    new_income = Income(
        user_id=user_id,
        amount=data['amount'],
        notes=data.get('note', '')  # Optional field
    )

    db.session.add(new_income)
    db.session.commit()

    return jsonify({"message": "Income created successfully"}), 201

# Update an income record
@income_bp.route('/update_income', methods=['PUT'])
@jwt_required()
def update_income(income_id):
    pass

# Delete an income record
@income_bp.route('/delete_income', methods=['DELETE'])
@jwt_required()
def delete_income(income_id):
    pass