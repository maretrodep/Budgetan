import json
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token
from backend import db
from backend.models.user import User
from . import auth_bp

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    profile_name = data.get('profile_name')
    password = data.get('password')

    if not email or not password or not profile_name:
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    user = User(profile_name=profile_name, email=email, role='user')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        identity = json.dumps({'id': user.id, 'role': user.role})
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({"message": "Invalid email or password"}), 401

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200

@auth_bp.route("/change_password", methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    new_password_repeat = data.get("new_password_repeat")

    if not current_password or not new_password or not new_password_repeat:
        return jsonify({"message": "Missing one of the fields"}), 400

    if new_password != new_password_repeat:
        return jsonify({"message": "New passwords don't match}"}), 400
    
    user_identity = get_jwt_identity()
    user = User.query.get(user_identity["id"])

    if not user or not user.check_password(current_password):
        return jsonify({"message": "Incorrect current password"}), 401

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200