from flask import Blueprint
from controllers.user_controller import create_user, authenticate_user
from controllers.password_controller import create_password

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["POST"]) #important
def sign_up():
    return "Hello world"

@auth_bp.route("/signin", methods=["POST"])   #important
def sign_in():
    return "Hello world"

@auth_bp.route("/signout", methods=["POST"])   #important
def sign_out():
    return "Hello world"
