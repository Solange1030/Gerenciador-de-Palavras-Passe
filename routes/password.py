from flask import Blueprint

password_bp = Blueprint("password", __name__, url_prefix="/passwords")

@password_bp.route("/", methods=["GET"])
def fetch_all():
    return "Hello world"

@password_bp.route("/<password_id>", methods=["GET"])   #important
def get_password(password_id):
    return "Hello world"

@password_bp.route("/", methods=["POST"])   #important
def add_password():
    return "Hello world"

@password_bp.route("/", methods=["PATCH"])  #important
def update_password():
    return "Hello world"

@password_bp.route("/", methods=["DELETE"])
def delete_password():
    return "Hello world"
