from extensions import db
from flask import jsonify
from controllers.service_controller import create_service
from models import Service, User, Password, Media
from utils import utils, stegano_utils, crypto


def create_password(data, file, email):
    try:
    
        service = Service.query.filter_by(designation=data["designation"]).first()

        if not service:
            new_service = create_service(data["designation"], data["url"])
            service = new_service[0] if isinstance(new_service, tuple) else new_service

        if not email:
            return jsonify({"message": "Email não encontrado"}), 404

        value_encrypted = crypto.encrypt_value(data["value"])

        exists = False
        all_passwords = Password.query.filter_by(user_email=email).all()

        for p in all_passwords:
            try:
                decrypted_value = crypto.decrypt_value(p.value)
                if decrypted_value == data["value"]:
                    exists = True
                    break
            except Exception:
                continue  

        password = Password(
            value=value_encrypted,
            category=data["category"],
            description=data["description"],
            user_email=email,
            service_id=service.id
        )

        db.session.add(password)
        db.session.commit()

        data_file = utils.upload_image(file)
        image_path = stegano_utils.embed_pass_in_image(value_encrypted, data_file["path"])
        stego_path = stegano_utils.saving_stegno_file(data_file["name"], data_file["upload_folder"], image_path)

        media = Media(
            _type_="Imagem",
            file_name=data_file["name"],
            password_id=password.id,
            path_file=stego_path
        )

        db.session.add(media)
        db.session.commit()

        if exists:
            return jsonify({"message": "Palavra-passe registada com sucesso (já existia uma igual armazenada)."}), 208
        else:
            return jsonify({"message": "Palavra-passe registada com sucesso."}), 200

    except Exception as e:
        return jsonify({"error": f"Falha ao registar: {str(e)}"}), 400

    

def show_password(service_id, email, code_validate):
    
    try:
        if not code_validate:
            return jsonify({"message": "Chave de acesso obrigatória"}), 400

        if not checking_secret_key(code_validate, email):
            return jsonify({"message": "Chave de acesso inválida"}), 403

        password = Password.query.filter((Password.service_id == service_id) & (Password.user_email == email) ).first()
        service = Service.query.filter_by(id = service_id).first()
        media = Media.query.filter_by(password_id = password.id).first()

        password_value = crypto.decrypt_value(password.value)
        if not password:
            return jsonify({"message": "Palavra-Passe não encontrada"}), 404

        response_data = {
            "password": password_value,
            "url": service.url,
            "designation": service.designation,
            "category": password.category,
            "description": password.description,
            "media_path": media.path_file,
            "email": email
        }
        
        if not password:
            return jsonify({"message": "Palavra-passe não decifrada"}), 400

        return jsonify({
                    "message": "sucesso",
                    "data": response_data
                }), 200
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {str(e)}"}), 400


def checking_secret_key(code_validate, email):
   
    user = User.query.filter_by(email = email).first()
    secret_key = crypto.decrypt_value(user.password_master)
    if secret_key == code_validate:
        return True, 200
    else:
        return False, 400
    

