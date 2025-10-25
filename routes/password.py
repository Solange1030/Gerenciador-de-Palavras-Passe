from flask import Blueprint, request
from controllers import password_controller
from utils.token_utils import token_required

password_bp = Blueprint("password", __name__, url_prefix="/passwords")


@password_bp.route("/", methods=["GET"])
def fetch_all():
    return "Hello world"

@password_bp.route("/<int:service_id>", methods=["POST"])   #important
@token_required
def get_password( email, service_id,):
    data = request.get_json() or {}
    code_validate = data.get("secret_key")
    return password_controller.show_password(service_id, email,  code_validate)


# @password_bp.route("/secret_key", methods = ["POST"])
# @token_required
# def check_secret_key():
#     code_validate = request.get_json()
#     return password_controller.checking_secret_key(code_validate)


@password_bp.route("/add_pass", methods=["POST"])   #important
@token_required
def add_password(email):
    data = request.form.to_dict()         
    file = request.files.get("image") 
    return password_controller.create_password(data, file, email)


@password_bp.route("/", methods=["PATCH"]) 
def update_password():
    return "Hello world"

@password_bp.route("/", methods=["DELETE"])
def delete_password():
    return "Hello world"
