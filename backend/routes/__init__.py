from flask import Blueprint

# Define blueprints
auth_bp = Blueprint('auth', __name__)
income_bp = Blueprint('income', __name__)
expense_bp = Blueprint('expense', __name__)


# Import route handlers
from .auth import *
from .income import *
from .expense import *