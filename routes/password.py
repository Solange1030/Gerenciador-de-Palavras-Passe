from flask import Blueprint, request
from controllers import password_controller
from utils.token_utils import token_required

password_bp = Blueprint("password", __name__, url_prefix="/passwords")


@password_bp.route("/", methods=["GET"])
def fetch_all():
    return "Hello world"

@password_bp.route("/<int:media_id>", methods=["GET"])   #important
def get_password(media_id):
    return password_controller.show_password(media_id)


@password_bp.route("/secret_key", methods = ["POST"])
def check_secret_key():
    code_validate = request.get_json()
    return password_controller.checking_secret_key(code_validate)


@password_bp.route("/add_pass", methods=["POST"])   #important
def add_password():
    data = request.form.to_dict()         
    file = request.files.get("image") 
    return password_controller.create_password(data, file)

@password_bp.route("/list_pass", methods=["GET"])   #important
def list_password():
    data = request.form.to_dict()         
    file = request.files.get("image") 
    return password_controller.create_password(data, file)


@password_bp.route("/", methods=["PATCH"]) 
def update_password():
    return "Hello world"

@password_bp.route("/", methods=["DELETE"])
def delete_password():
    return "Hello world"
