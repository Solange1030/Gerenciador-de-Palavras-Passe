import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify
from models.User import User
import jwt
import datetime

SECRET_KEY = os.getenv("SECRET_KEY")

def generate_token(user):
    payload = {
        "email": user.email,  
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),  
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return jsonify({"message": "Token não encontrado"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            email = data["email"] 
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401

        
        return f(email, *args, **kwargs)

    return decorated
