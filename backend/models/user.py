from werkzeug.security import generate_password_hash, check_password_hash
from backend import db
from ..config import DatabaseConfig

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(DatabaseConfig.TEXT_SIZE), nullable=False, default='user')
    profile_name = db.Column(db.String(DatabaseConfig.TEXT_SIZE), nullable=False)
    email = db.Column(db.String(DatabaseConfig.TEXT_SIZE), unique=True, nullable=False)
    password_hash = db.Column(db.String(DatabaseConfig.HASH_SIZE), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)
    incomes = db.relationship('Income', backref='user', lazy=True)

    def set_password(self, password):
        """Hash the password and store it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the stored hash."""
        return check_password_hash(self.password_hash, password)