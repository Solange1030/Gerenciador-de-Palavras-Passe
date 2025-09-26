from app import db

class Service(db.Model):
    __tablename__ = "Services"
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())