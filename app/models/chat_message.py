from app import db
from datetime import datetime, timezone

class Chat_message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender = db.Column(db.String, nullable = False)
    message = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default = False)
