from flask import Blueprint, jsonify, request

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("/", methods=["GET"])
def get_users():
    return "Hello world"

@user_bp.route("/me", methods=["GET"])   #important
def get_user():
    return "Hello world"

@user_bp.route("/", methods=["POST"])   #important
def add_user():
    return "Hello world"

@user_bp.route("/", methods=["PATCH"])  #important
def update_user():
    return "Hello world"

@user_bp.route("/", methods=["DELETE"])
def delete_user():
    return "Hello world"
