from flask import Blueprint
from controllers import media_controller 

# 
media_bp = Blueprint("media", __name__, url_prefix="/medias")

# @media_bp.route("/<string:email>", methods=["GET"])
# def fetch_all():
#     return "Hello world"

# @media_bp.route("/<media_id>", methods=["GET"])   #important
# def get_media(media_id):
#     return "Hello world"

# @media_bp.route("/", methods=["POST"])   #important
# def add_media():
#     return "Hello world"

# @media_bp.route("/", methods=["PATCH"])  #important
# def update_media():
#     return "Hello world"

# @media_bp.route("/", methods=["DELETE"])
# def delete_media():
#     return "Hello world"
