from app import db
from models.User import User
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(name,email, password_master):
    user = User.query.filter_by(email=email).first()
    if not user:
        try:
            password_hashed = generate_password_hash(password_master)
            user = User(name=name, email=email, password_master = password_hashed)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        raise ValueError("Email ja existente, tente com outro")
    

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_master, password):
        print("encontrado")
        return user
    return None



