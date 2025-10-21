import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify
from models.User import User

SECRET_KEY = os.getenv("SECRET_KEY")

def generate_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
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
    """Decorador para proteger rotas"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')  # pega token do cookie

        if not token:
            return jsonify({'message': 'Token ausente'}), 401

        data = verify_token(token)
        if not data:
            return jsonify({'message': 'Token inválido ou expirado'}), 401

        current_user = User.query.get(data['user_id'])
        if not current_user:
            return jsonify({'message': 'Usuário não encontrado'}), 404

        # passa o usuário autenticado para a função protegida
        return f(current_user, *args, **kwargs)
    return decorated
