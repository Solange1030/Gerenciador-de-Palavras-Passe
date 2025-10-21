from flask import Flask
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from extensions import db

load_dotenv()

def create_app():
    app = Flask(__name__)

    db_user = os.getenv("DB_USER")
    db_host = os.getenv("DB_HOST")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_user}{':' + db_password if db_password else ''}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    db.init_app(app)
    Migrate(app, db)

    # Importa os modelos aqui
    from models.User import User
    from models.Password import Password
    from models.Media import Media
    from models.Service import Service

    # Importa Blueprints aqui
    from routes.user import user_bp
    from routes.password import password_bp
    from routes.auth import auth_bp
    from routes.main import main_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(password_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    #print("✅ Blueprints registrados com sucesso!")

    return app
