import json
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend import db, jwt
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
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid email or password"}), 401