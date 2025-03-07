from flask import Blueprint

# Define blueprints
auth_bp = Blueprint('auth', __name__)
income_bp = Blueprint('income', __name__)


# Import route handlers
from .auth import *
from .income import *