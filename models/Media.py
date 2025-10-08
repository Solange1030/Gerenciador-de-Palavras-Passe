from app import db

class Media(db.Model):
    __tablename__ = "media"
    id = db.Column(db.Integer, primary_key=True)
    _type_ = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    path_file = db.Column(db.String(100), nullable=False)
    password_id = db.Column(db.Integer, db.ForeignKey("passwords.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())
    