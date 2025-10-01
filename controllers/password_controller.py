from app import db
from models.Password import Password
from controllers.service_controller import create_service
from models.Service import Service
from models.User import User
from werkzeug.security import generate_password_hash, check_password_hash

def create_password( value, category, description, designation, url, user_email):
    service = Service.query.filter_by(designation = designation).first()
    email = User.query.filter_by(email = user_email).first()
    value_hashed = generate_password_hash(value)

    if not email:
       raise ValueError("Utilizador nao encontrado")
    if not service:
       service = create_service( designation, url)
    
    try:
        password = Password(
            value = value_hashed,
            category = category,
            description = description,
            user_email = email.email,
            service_id = service.id
        )
        db.session.add(password)
        db.session.commit()
        return password
    except Exception as e:
        db.session.rollback()
        raise e
    
