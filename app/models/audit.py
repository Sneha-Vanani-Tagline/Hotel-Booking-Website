from app import db
from datetime import date, datetime, timezone

class Audit_logs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    action = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_cred.id'), nullable = False)

    record_id = db.Column(db.Integer, nullable = True)
    table_name = db.Column(db.String(100), nullable = True)
    field = db.Column(db.String(100), nullable = True)
    old_value = db.Column(db.String(255), nullable = True)
    new_value = db.Column(db.String(255), nullable = True)

    timestamp = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc), nullable = False)
