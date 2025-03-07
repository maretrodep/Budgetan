from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend import db
from backend.models.income import Income
from . import income_bp

# Create a new income record
@income_bp.route('/add_income', methods=['POST'])
@jwt_required()
def add_income():
    pass

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