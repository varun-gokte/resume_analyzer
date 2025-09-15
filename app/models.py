from .extensions import db
from datetime import datetime, timezone

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    filepath = db.Column(db.String(255),nullable=False)
    mimetype = db.Column(db.String(100),nullable=False)
    size = db.Column(db.Integer)
    parsed_text = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))