from flask import Blueprint, jsonify
from utils.token_utils import token_required

main_bp = Blueprint("main", __name__, url_prefix="/")

@token_required
@main_bp.route("/dashboard", methods=["GET"])
def index():
    return jsonify({"message": "Welcome 3S - Password manager"})
