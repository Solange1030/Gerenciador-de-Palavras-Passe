from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/stegano_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # models importadas
    from models.User import User
    from models.Service import Service
    from models.Password import Password
    from models.Media import Media
    from models.User_Auth import User_Auth
    

    Migrate(app, db)
    
    print('connectou')
    return app

