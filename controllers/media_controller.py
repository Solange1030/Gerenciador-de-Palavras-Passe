from PIL import Image
from extensions import db
from flask import jsonify
from models.Media import Media
from models import Password
from utils import utils


def create_media(value_hashed, password_id, img: Image.Image):

    password = Password.query.filter_by(id = password_id)
    if not password:
        raise ValueError("Palavra-passe \n encontrada")
    
    password_in_bytes = value_hashed.encode("utf-8")
    image = utils.embed_pass_in_image( password_in_bytes, img )
    upload = utils.upload_image_controller(image)

    if upload == True:
        return jsonify({"message": "Imagem armazenada"}), 200
    
    try:
        dataMedia = utils.getting_path_filename(image)
        media = Media(
            _type_ = "Imagem",
            file_name = dataMedia["filename"],
            password_id = password.id,
            path_file = dataMedia["path"]
        )

        db.session.add(media)
        db.session.commit()
        return jsonify({"message": "Imagem armazenada"}), 200
    except Exception as e:
        db.session.rollback()
        raise e
    






