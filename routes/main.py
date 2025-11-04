from flask import Blueprint, jsonify
from utils.token_utils import token_required
from controllers import main_controller

main_bp = Blueprint("main", __name__, url_prefix="/")

# @main_bp.route("/", methods=["GET"])
# def index():
#     return jsonify({"message": "Welcome to 3s-Threes Password"})

@main_bp.route("/dashboard", methods=["GET"])
@token_required
def dashboard(email):
   
    return main_controller.list_dash(email)
