from flask import jsonify, request, Response
from app import db
from models import User
from utils import utils

def sign_up (request):
    response = {
        "status": "Error",
        "message": "",
        "data": {},
    }

    data = request.get_json(silent=True)
    if not data:
        response["message"] = "Por favor, envie um json valido."
    else:
        if "name" not in data or not data["name"]:
            response["message"] = "Por favor, insira um nome válido."
        elif "email" not in data or ("@" not in data["email"] or len(data["email"]) < 8):
            response["message"] = "Por favor, insira um email válido."
        else:
            user = User(email=data["email"], name=data["name"]);

            try:
                db.session.add(user)
                db.session.commit();

                response["status"] = "Ok"
                response["message"] = "Conta criada com sucesso."
                response["data"] = user.to_dict();
            except Exception as e:
                db.session.rollback();
                response["status"] = "Error"
                response["message"] = str(e.__cause__)
                response["data"] = {};
    
    return jsonify(response)

def sign_in(data):
    user = User.query.filter_by(email = data["email"]).first()
    otp = utils.gen_otp()
    # user
