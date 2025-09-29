from flask import Blueprint, jsonify, request
from controllers.UserController import create_user, authenticate_user
from controllers.PasswordController import create_password

user_api = Blueprint("user_api", __name__)

@user_api.route("/user", methods=["POST"])
def add_user():
    data = request.json
    create_user(data["name"], data["email"], data["password"])
    return jsonify({"message:", "Dados registados"})

@user_api.route("/login", methods=["POST"])
def login_auth():
    data = request.json
    user = authenticate_user(data["email"], data["password"])
    return jsonify()

@user_api.route("/password", methods = ["POST"])
def add_pass():
    data = request.json
    create_password(data["value"], data["category"], data["description"], data["designation"], data["url"], data["user_email"])
    return jsonify({"message:", "Palavra-Passe registada"})

# @user_api.route("/home", methods=["POST"])
# def 