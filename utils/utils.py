import secrets
import unicodedata
from flask import  current_app
from werkzeug.utils import secure_filename
import os
from PIL import Image
import string
import random
from flask_mail import Message
from app.create_app import app

#gerar codigo OTP
def gen_otp():
    otp = secrets.randbelow(900000) + 100000
    return str(otp)

#gerar chave_secreta

def key_gen(length = 8):
    characters = string.ascii_letters + string.digits  
    code = ''.join(random.choices(characters, k=length))
    return code

#upload files
def upload_image(file):
    
    filename = secure_filename(file.filename)
    filename = unicodedata.normalize("NFKD", filename).encode("ascii", "ignore").decode("ascii")

    base_upload_folder = current_app.config['UPLOAD_FOLDER']
    original_folder = os.path.join(base_upload_folder, "original_files")
    os.makedirs(original_folder, exist_ok=True)

    filename = os.path.splitext(filename)[0] + ".png"

    file_path = os.path.join(original_folder, filename)

    if os.path.exists(file_path):

        print("Imagem ja existente")
        data = {
            "upload_folder" : base_upload_folder,
            "path" : file_path,
            "name" : filename
        }
        return  data
    
    else:
        image = Image.open(file)
        image.save(file_path, format="PNG")

        data = {
            "upload_folder" : base_upload_folder,
            "path" : file_path,
            "name" : filename
        }
        return data

    
def send_email(email, name, otp_code):
    msg = Message(
        subject="Seu código OTP",
        recipients=[email],
        body=f"Olá {name},\n\nO seu código OTP é: {otp_code}\n\nUse-o para continuar o login."
    )
    
    Thread(target=send_async_email, args=(app, msg)).start()
