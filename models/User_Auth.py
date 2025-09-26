from app import db

class User_Auth(db.Model):
    __tablename__ = "User_Auth"
    id = db.Column(db.Integer, primary_key=True)
    password_master = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(50), db.ForeignKey("Users.email"), nullable=False)