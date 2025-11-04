from models import User, Password, Service, Media
from flask import jsonify

from utils import crypto


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
    counter_media = 0
    counter_repeated = 0 

    try:
        passwords = Password.query.filter_by(user_email=email).all()
        seen_passwords = {}

        for p in passwords:
            counter_passwords += 1

            media = Media.query.filter_by(password_id=p.id).first()
            if media:
                counter_media += 1

            try:
                decrypted_value = crypto.decrypt_value(p.value)
            except Exception:
                decrypted_value = None  # caso falhe a desencriptação

            if decrypted_value:
                if decrypted_value in seen_passwords:
                    seen_passwords[decrypted_value] += 1
                else:
                    seen_passwords[decrypted_value] = 1

        for count in seen_passwords.values():
            if count > 1:
                counter_repeated += count

        return jsonify({
            "passwords": counter_passwords,
            "media": counter_media,
            "repeated": counter_repeated
        }), 200

    except Exception as e:
        return jsonify({"error": f"Falha ao buscar: {str(e)}"}), 400


        
