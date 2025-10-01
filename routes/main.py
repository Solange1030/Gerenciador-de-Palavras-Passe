from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__, url_prefix="/")

@main_bp.route("", methods=["GET"])
def index():
    return jsonify({"message": "Welcome 3S - Password manager"})
