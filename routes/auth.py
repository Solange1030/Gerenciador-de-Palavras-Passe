from flask import Blueprint, request
from controllers import auth_controller
from controllers.password_controller import create_password
from utils.token_utils import token_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["POST"]) #important
def sign_up():
    data = request.get_json()
    return auth_controller.sign_up(data)

@auth_bp.route("/signin", methods=["POST"])   #important
def sign_in():
    data = request.get_json()
    return auth_controller.sign_in(data)

# @auth_bp.route("/", methods=["POST"])   #important
# def sign_in():
#     data = request.get_json()
#     return auth_controller.sign_in(data)


@auth_bp.route("/check_otp", methods=["POST"])   #important
def check_otp():
    otp = request.get_json()
    
    return auth_controller.otp_varificate(otp)

@auth_bp.route("/signout", methods=["POST"])   #important
def sign_out():
    return "Hello world"

