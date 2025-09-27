from flask import Blueprint, jsonify, request
from controllers.UserController import create_user, authenticate_user

user_api = Blueprint("user_api", __name__)

@user_api.route("/user", methods=["POST"])
def add_user():
    data = request.json
    create_user(data["name"], data["surname"], data["email"], data["password"])
    return jsonify({"message:", "Dados registados"})

@user_api.route("/login", methods=["POST"])
def login_auth():
    data = request.json
    user = authenticate_user(data["email"], data["password"])
    return jsonify()
