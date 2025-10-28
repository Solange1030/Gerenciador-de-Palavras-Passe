from extensions import db
from flask import jsonify
from controllers.service_controller import create_service
from models import Service, User, Password, Media
from utils import utils, stegano_utils, crypto


def create_password(data, file, email):
    service = Service.query.filter_by(designation = data["designation"]).first()

    value_encrypted = crypto.encrypt_value(data["value"])

    if not email:
        return jsonify({"message": "Email nao encontrado"}), 404
    if not service:
       service = create_service( data["designation"], data["url"])
    
    try:
        password = Password(
            value = value_encrypted,
            category = data["category"],
            description = data["description"],
            user_email = email,
            service_id = service.id
        )

        db.session.add(password)
        db.session.commit()

        data_file = utils.upload_image(file)

        image_path = stegano_utils.embed_pass_in_image(value_encrypted, data_file["path"])

        stego_path = stegano_utils.saving_stegno_file(data_file["name"], data_file["upload_folder"], image_path)

        media = Media(
            _type_= "Imagem",
            file_name= data_file["name"],
            password_id= password.id,
            path_file= stego_path
        )

        db.session.add(media)
        db.session.commit()

        return jsonify({"message": "Registado"}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao registar: {str(e)}"}), 401
    

def show_password(service_id, email, code_validate):
    
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

    response = [ ]
    response.append({
        "password": password_value,
        "url": service.url,
        "designation": service.designation,
        "category": password.category,
        "description": password.description,
        "media_path": media.path_file,
        "email": email
    })
    if not password:
        return jsonify({"message": "Palavra-passe não decifrada"}), 400

    return response, 200



# def patch_password(email, password_id, data):
    
#     password = Password.query.filter_by(id=password_id, user_email=email).first()

#     if not password:
#         return jsonify({"message": "Senha não encontrada"}), 404

#     # Atualiza apenas o que foi enviado
#     if "category" in data:
#         password.category = data["category"]
#     if "description" in data:
#         password.description = data["description"]
#     if "value" in data:
#         password.value = crypto.encrypt_value(data["value"])

#     db.session.commit()
#     return jsonify({"message": "Senha atualizada parcialmente com sucesso"})


def checking_secret_key(code_validate, email):
   
    user = User.query.filter_by(email = email).first()
    secret_key = crypto.decrypt_value(user.password_master)
    if secret_key == code_validate:
        return True, 200
    else:
        return False, 400
    

