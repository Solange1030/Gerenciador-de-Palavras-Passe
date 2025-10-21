from extensions import db
from flask import jsonify, make_response, redirect, url_for
from models import User
from utils import utils, crypto
from email_validator import validate_email, EmailNotValidError
from utils import token_utils


def sign_up (data):
    try:
        try:
            valid = validate_email(data["email"])
            data["email"] = valid.email

        except EmailNotValidError as e:
            return jsonify({"error": str(e)}), 400
        
        #secret_key = utils.key_gen()
        user = User(
            name = data["name"],
            email = data["email"],
            password_master = crypto.encrypt_value(data["password_master"]),
            otp_code = ""

        )

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Bem vinda " + user.name + ". Guarde a sua chave-mestra para acessar a todas as palavras-passe armazenadas"})
    
    except Exception  as e:
        db.session.rollback()
        raise e

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
        #jsonify({"message": "OTP gerado, ", "otp": user.otp_code})
        return jsonify({"message": "OTP gerado, ", "otp": user.otp_code})
    else:
        return jsonify({"message": "Email nao achado "})   

def otp_varificate(otp_data):

    otp_required = otp_data.get("otp")
    user = User.query.filter_by( otp_code = otp_required).first()
    if user:
        user.otp_code = ""
        token = token_utils.generate_token(user)
        resp = make_response(redirect(url_for("main.index")))
        resp.set_cookie('token', token, httponly=True, samesite='Strict', max_age=7200)
        return resp
    else:
        return jsonify({"message": "Invalido OTP"}), 401


