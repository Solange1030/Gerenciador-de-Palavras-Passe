from extensions import db
from flask import jsonify
from controllers.service_controller import create_service
from models import Service, User, Password, Media
from utils import utils, stegano_utils, crypto


def create_password(data, file, email):
    service = Service.query.filter_by(designation = data["designation"]).first()

    value_encrypted = crypto.encrypt_value(data["value"])

    if not email:
       raise ValueError("Utilizador nao encontrado")
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

        return jsonify({"message": "Registado"})
    except Exception as e:
        db.session.rollback()
        raise e
    

def show_password(file_id, email, data, code_validate):
    
    if not code_validate:
        return jsonify({"message": "Chave de acesso obrigatória"}), 400

    if not checking_secret_key(code_validate, email):
        return jsonify({"message": "Chave de acesso inválida"}), 403

    media = Media.query.filter_by(id=file_id).first()
    if not media:
        return jsonify({"message": "Arquivo não encontrado"}), 404

    password = stegano_utils.extrating_password(media.path_file)
    if not password:
        return jsonify({"message": "Palavra-passe não decifrada"}), 400

    decrypted_pass = crypto.decrypt_value(password)
    return jsonify({"message": f"Palavra-passe: {decrypted_pass}"})



def list_services(email):
    
#     passwords = Password.query.filter_by(user_email = email).all()

    result=[]
#     for p in passwords:
#         service = Service.query.filter_by(id = p.id).first()
        
#         result.append({
#             "service_id": service.id,
#             "service_designation": service.designation,
#             "service_url": service.url
#         })
    return result

def checking_secret_key(code_validate, email):
    user = User.query.filter(
        (User.password_master == code_validate) & (User.email == email)
    ).first()

    return user is not None
    

