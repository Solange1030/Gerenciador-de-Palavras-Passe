from flask import Blueprint, jsonify
from utils.token_utils import token_required
from controllers import main_controller

main_bp = Blueprint("main", __name__, url_prefix="/")


@main_bp.route("/dashboard", methods=["GET"])
@token_required
def index(email):
    name = main_controller.index(email)
    return jsonify({"message": "Hello, "+ name +". Welcome 3S - Password manager"})
