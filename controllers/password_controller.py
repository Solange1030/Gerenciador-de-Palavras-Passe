from app import db
from flask import jsonify
from controllers.service_controller import create_service
from models import Service, User, Password, Media
from utils import utils, stegano_utils, crypto


def create_password(data, file):
    service = Service.query.filter_by(designation = data["designation"]).first()
    email = User.query.filter_by(email = data["email"]).first()

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
            user_email = email.email,
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
    
def show_password(file_id):

    media = Media.query.filter_by(id = file_id).first()
    
    if not media:
        return jsonify({"message": "Not Found"})
    
    password = stegano_utils.extrating_password(media.path_file)

    if password == False:
        return jsonify({"message": "Palavra-passe nao decifrada"})
    else:
        
        unencripted_pass = crypto.decrypt_value(password)
        return jsonify({"message": "Palavra-passe: "+ unencripted_pass})
    


    
#def checking_secret_key(code_validate):

