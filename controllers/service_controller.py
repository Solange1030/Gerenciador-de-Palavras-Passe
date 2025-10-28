from flask import jsonify
from extensions import db
from models.Service import Service

def create_service( designation, url):
    try:
        service = Service(designation = designation, url = url)
        db.session.add(service)
        db.session.commit()
        return service, 200    
    except Exception as e:
        return jsonify({"message": "Palavra-Passe não encontrada"}), 404