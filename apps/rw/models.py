import datetime
from sqlalchemy.dialects.mysql import LONGTEXT

from apps.models import db


class RWData(db.Model):
    __tablename__ = 'rw_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(LONGTEXT, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
