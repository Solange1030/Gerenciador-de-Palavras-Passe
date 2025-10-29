from models import User, Password, Service, Media
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
    
def list_dash(email):
    counter_passwords = 0 
    counter_media= 0
    try:
        passwords = Password.query.filter_by(user_email = email).all()
        
        for p in passwords:
            media =Media.query.filter_by(password_id = p.id).first()
            if media:
                counter_media = counter_media+1
            counter_passwords= counter_passwords+1
        
        return jsonify({
            "passwords": counter_passwords,
            "media": counter_media
        }), 200

            
    
    except Exception as e:
        return jsonify({"error": f"Falha ao buscar: {str(e)}"}), 400
        