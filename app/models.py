from datetime import datetime
from app import db

class IOC(db.Model):
    __tablename__ = "ioc"

    id = db.Column(db.Integer, primary_key=True)
    ioc_value = db.Column(db.String(255), nullable=False)
    ioc_type = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(100))
    threat_type = db.Column(db.String(50))
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)

    attack_technique = db.Column(db.String(20))

    def __repr__(self):
        return f"<IOC {self.ioc_value}>"
