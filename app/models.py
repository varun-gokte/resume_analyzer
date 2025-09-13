from .extensions import db
from datetime import datetime, timezone

class File(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    filepath = db.Column(db.String(255),nullable=False)
    mimetype = db.Column(db.String(100),nullable=False)
    size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))