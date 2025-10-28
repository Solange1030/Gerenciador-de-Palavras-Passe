from flask import Blueprint, request, jsonify
from controllers import auth_controller
from controllers.password_controller import create_password
from utils.token_utils import token_required
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["POST"]) #important
def sign_up():
    return auth_controller.sign_up(request)

@auth_bp.route("/signin", methods=["POST"])   #important
def sign_in():
    data = request.get_json()
    return auth_controller.sign_in(data)



@auth_bp.route("/check_otp", methods=["POST"])   #important
def check_otp():
    otp = request.get_json()
    
    return auth_controller.otp_varificate(otp)


@auth_bp.route("/user_data", methods=["GET"])
@token_required
def get_user_data(email):
    user = User.query.filter_by(email=email).first()
    return jsonify({"email": user.email, "id": user.id})

@auth_bp.route("/signout", methods=["POST"])   #important
def sign_out():
    return "Hello world"

