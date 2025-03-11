from backend import db
from datetime import datetime
from config import DatabaseConfig

class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    category = db.Column(db.String(DatabaseConfig.TEXT_SIZE), nullable=False)
    priority = db.Column(db.String(DatabaseConfig.TEXT_SIZE), nullable=False)
    status = db.Column(db.String(DatabaseConfig.TEXT_SIZE), nullable=False)
    mood = db.Column(db.String(DatabaseConfig.TEXT_SIZE), nullable=False)
    tags = db.Column(db.String(DatabaseConfig.TEXT_SIZE))
    note = db.Column(db.Text)