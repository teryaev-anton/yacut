from datetime import datetime

from . import db

from .constants import USER_INPUT_LIMIT


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, unique=False, nullable=False)
    short = db.Column(db.String(USER_INPUT_LIMIT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
