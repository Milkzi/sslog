import datetime

from apps.models import db



class ShengShengLog(db.Model):
    __tablename__ = 'ss_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(20), nullable=False)
    log_info = db.Column(db.String(500), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.datetime.now())