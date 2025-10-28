from extensions import db

class Password(db.Model):
    __tablename__ = "passwords"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    user_email = db.Column(db.String(100), db.ForeignKey("users.email"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())
