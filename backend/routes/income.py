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
        note=data.get('note', '')  # Optional field
    )

    db.session.add(new_income)
    db.session.commit()

    return jsonify({"message": "Income created successfully"}), 201

# Update an income record
@income_bp.route('/update_income', methods=['PUT'])
@jwt_required()
def update_income(income_id):
    income_id = request.args.get('id')
    user_id = get_jwt_identity()
    data = request.get_json()

    if not income_id:
        return jsonify({"message": "Income ID is required"}), 400

    income = Income.query.filter_by(id=income_id, user_id=user_id).first()
    if not income:
        return jsonify({"message": "Income not found"}), 404

    # Update the income record
    if 'amount' in data:
        income.amount = data['amount']
    if 'note' in data:
        income.note = data['note']

    db.session.commit()

    return jsonify({"message": "Income updated successfully"}), 200

@income_bp.route('/delete_incomes', methods=['DELETE'])
@jwt_required()
def delete_incomes():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate the request data
    if not data or 'income_ids' not in data:
        return jsonify({"message": "Income IDs are required"}), 400

    income_ids = data['income_ids']

    # Fetch and delete the income records
    incomes = Income.query.filter(Income.id.in_(income_ids), Income.user_id == user_id).all()
    if not incomes:
        return jsonify({"message": "No matching incomes found"}), 404

    if len(income_ids) != len(incomes):
        return jsonify({"message": "Some of the income ids don't exist"}), 400
    
    for income in incomes:
        db.session.delete(income)

    db.session.commit()

    if len(incomes) == 1:
        message = "income deleted successfully"
    else:
        message = f"{len(incomes)} incomes deleted successfully"

    return jsonify({"message": message}), 200