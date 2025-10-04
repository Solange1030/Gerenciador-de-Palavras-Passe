from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

db = SQLAlchemy()
app = Flask(__name__)

def create_app():

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_user}{':' + db_password if db_password else ''}@{db_host}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # models importadas
    from models.Password import Password
    from models.Media import Media  
    from models.User import User
    from models.Service import Service

    from routes.user import user_bp
    from routes.password import password_bp
    from routes.auth import auth_bp
    from routes.main import main_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(password_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    Migrate(app, db)
    print('connectou')
    return app

