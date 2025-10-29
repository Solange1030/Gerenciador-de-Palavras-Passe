from models import User, Password, Service
from flask import jsonify


def index(email):
    try:
        pass_data = Password.query.filter_by(user_email=email).all()
        user = User.query.filter_by(email = email).first()
        if not user:
            return jsonify({"message": "Email não encontrado"}), 404
        
        result = []
        for p in pass_data:
            service = Service.query.filter_by(id = p.service_id).first()
            result.append({
                "service_id": service.id if service else None,
                "service_name": service.designation if service else None,
                "service_url": service.url if service else None,
                "user_name": user.name
            })
    
        return jsonify({
                        "data": result,
                        "status": 200
                    })
    except Exception as e:
        return jsonify({"error": str(e)}), 500