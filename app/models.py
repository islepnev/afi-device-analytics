from .db import db
from datetime import datetime

class HwFirmware(db.Model):
    __tablename__ = 'hw_firmware'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    revision = db.Column(db.Integer)
    fw_maj = db.Column(db.Integer)
    fw_min = db.Column(db.Integer)
    git_hash = db.Column(db.String(40))
    base_name = db.Column(db.String(40), nullable=False)
    pcb_name = db.Column(db.String(20))
    path = db.Column(db.Text, nullable=False)
    fromHost = db.Column(db.Text, nullable=False)
    goldImg = db.Column(db.Boolean, nullable=False)
    serialHex = db.Column(db.String(255), nullable=False)
