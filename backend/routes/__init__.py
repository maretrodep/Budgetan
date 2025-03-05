# app/routes/__init__.py
from flask import Blueprint

# Define blueprints
auth_bp = Blueprint('auth', __name__)

# Import route handlers
from .auth import *