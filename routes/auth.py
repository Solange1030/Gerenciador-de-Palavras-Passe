from flask import Blueprint, request
from controllers import auth_controller
from controllers.password_controller import create_password

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["POST"]) #important
def sign_up():
    data = request.get_json()
    return auth_controller.sign_up(data)

@auth_bp.route("/signin", methods=["POST"])   #important
def sign_in():
    return "Hello world"

@auth_bp.route("/check_otp", methods=["POST"])   #important
def check_otp():
    return "Hello world"

@auth_bp.route("/signout", methods=["POST"])   #important
def sign_out():
    return "Hello world"
