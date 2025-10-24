from models import User
from flask import jsonify


def index(email):
    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({"message": "Utilizador nao achado"})
    return  user.name