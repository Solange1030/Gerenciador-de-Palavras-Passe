from flask import jsonify
from extensions import db
from models.Service import Service

def create_service( designation, url):
    try:
        service = Service(designation = designation, url = url)
        db.session.add(service)
        db.session.commit()
        return service
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar serviço: {e}")
        return None