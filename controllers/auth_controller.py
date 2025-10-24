from extensions import db
from flask import jsonify, make_response, redirect, url_for
from models import User
from utils import utils, crypto
from email_validator import validate_email, EmailNotValidError
from utils import token_utils

from extensions import mail

def sign_up (data):
    try:
        try:
            valid = validate_email(data["email"])
            data["email"] = valid.email

        except EmailNotValidError as e:
            return jsonify({"error": str(e)}), 400
        
        
        code_otp = utils.gen_otp()
        user = User(
            name = data["name"],
            email = data["email"],
            password_master = crypto.encrypt_value(data["password_master"]),
            otp_code = code_otp

        )

        db.session.add(user)
        db.session.commit()
       
        mail.send(utils.send_email(user.email, user.name, user.otp_code))
        return jsonify({"message": "Bem vindo/a " + user.name + ". Guarde a sua chave-mestra para acessar a todas as palavras-passe armazenadas. Codigo enviado para o email" })

    except Exception  as e:
        db.session.rollback()
        return jsonify({"error": f"Falha ao registar: {str(e)}"}), 500


def sign_in(data):
    try:
        valid = validate_email(data["email"])
        data["email"] = valid.email

    except EmailNotValidError as e:
        return jsonify({"error": str(e)}), 400
    
    user = User.query.filter_by(email = data["email"]).first()

    if user:
        user.otp_code = utils.gen_otp()
        db.session.commit()
       
        try:
            mail.send(utils.send_email(user.email, user.name, user.otp_code))
            return jsonify({"message": "OTP gerado e enviado para o email"}), 200
        except Exception as e:
            return jsonify({"error": f"Falha ao enviar o email: {str(e)}"}), 500
    else:
        return jsonify({"message": "Email não encontrado"}), 404 


def otp_varificate(otp_data):
    otp_required = otp_data.get("otp")

    user = User.query.filter_by(otp_code=otp_required).first()

    if user:
        token = token_utils.generate_token(user)  

        resp = make_response(jsonify({
            "message": "OTP verificado com sucesso"
           
        }))
        resp.set_cookie(
            "token", token,
            httponly=True,
            samesite="Strict",
            max_age=7200
        )
      
        user.otp_code = ""
        db.session.add(user)
        db.session.commit()
        return resp

    else:
        return jsonify({"message": "OTP inválido"}), 401




