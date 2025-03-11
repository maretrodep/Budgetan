from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend import db
from backend.models.expense import Expense
from config import DatabaseConfig
from . import expense_bp

# Create a new expense record
@expense_bp.route('/add_expense', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    user_id = get_jwt_identity()

    is_valid, message, status_code = is_expense_valid(data)
    if not is_valid:
        return jsonify({"message": message}), status_code

    # Create a new expense record
    new_expense = Expense(
        user_id=user_id,
        amount=float(data['amount']),
        category=data['category'],
        priority=data['priority'],
        status=data['status'],
        mood=data['mood'],
        note=data.get('note', '')  # Optional field
    )

    db.session.add(new_expense)
    db.session.commit()

    return jsonify({"message": "Expense created successfully"}), 201

@expense_bp.route('/delete_expenses', methods=['DELETE'])
@jwt_required()
def delete_expenses():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate the request data
    if not data or 'expense_ids' not in data:
        return jsonify({"message": "Expense IDs are required"}), 400

    expense_ids = data['expense_ids']

    # Fetch and delete the expense records
    expenses = Expense.query.filter(Expense.id.in_(expense_ids), Expense.user_id == user_id).all()
    if not expenses:
        return jsonify({"message": "No matching expenses found"}), 404

    if len(expense_ids) != len(expenses):
        return jsonify({"message": "Some of the expense ids don't exist"}), 400
    
    for expense in expenses:
        db.session.delete(expense)

    db.session.commit()

    if len(expenses) == 1:
        message = "expense deleted successfully"
    else:
        message = f"{len(expenses)} expensess deleted successfully"

    return jsonify({"message": message}), 200

def is_expense_valid(data):
    required_fields = ['amount', 'category', 'priority', 'status', 'mood']
    for field in required_fields:
        if not data.get(field):
            return False, f"{field.capitalize()} is required", 400

    # Validate amount
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return False, "Amount must be a positive number", 400
    except ValueError:
        return False, "Amount must be a valid number", 400

    # Validate time (if provided)
    if 'time' in data:
        try:
            datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return False, "Time must be in the format 'YYYY-MM-DD HH:MM:SS'", 400

    # Validate priority
    valid_priorities = ['Essential', 'Optional']
    if data['priority'] not in valid_priorities:
        return False, "Priority must be either Essential or Optional", 400

    # Validate status
    valid_statuses = ['Pending', 'Paid']
    if data['status'] not in valid_statuses:
        return False, "Status must be either Pending or Paid", 400

    # Validate Category Size
    if len(data['category']) > DatabaseConfig.TEXT_SIZE:
        return False, f"Category is longer than {DatabaseConfig.TEXT_SIZE}", 422

    # Validate mood
    valid_moods = ['Happy', 'Sad']
    if data['mood'] not in valid_moods:
        return False, "Mood must be either Happy or Sad", 400

    return True, "Valid", 200
