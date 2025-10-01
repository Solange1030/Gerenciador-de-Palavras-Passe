from app import db
from models import User
from utils import utils

def sign_up (data):
    user = User(name = data["name"], email = ["email"])
    return user

def sign_in(data):
    user = User.query.filter_by(email = data["email"]).first()
    otp = utils.gen_otp()
    # user
