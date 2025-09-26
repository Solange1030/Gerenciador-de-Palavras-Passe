from app import db

class Password(db.Model):
    __tablename__ = "Passwords"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("Services.id"), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(50), db.ForeignKey("Users.email"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())
