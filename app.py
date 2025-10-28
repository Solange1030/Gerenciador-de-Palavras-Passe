from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv
from extensions import db, mail

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configurações do banco de dados
    db_user = os.getenv("DB_USER")
    db_host = os.getenv("DB_HOST")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_user}{':' + db_password if db_password else ''}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Uploads
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['FLASK_KEY'] = os.getenv("FLASK_KEY")

    # Configurações do Flask-Mail
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL", "False") == "True"
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")  # seu email
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")  # senha ou app password
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER", app.config['MAIL_USERNAME'])

    # Inicialização das extensões
    db.init_app(app)
    mail.init_app(app)
    Migrate(app, db)

    # CORS
    try:
        CORS(
            app,
            supports_credentials=True,      # MUITO IMPORTANTE para cookies
            origins=["http://localhost:5173"],  # frontend React
            methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["Content-Type", "Authorization"]
        )
        
        print("CORS ativado com sucesso")
    except Exception as e:
        print(f"Falha ao ativar CORS: {e}")

    # Importa modelos após inicializar o db
    from models.User import User
    from models.Password import Password
    from models.Media import Media
    from models.Service import Service

    # Importa blueprints
    from routes.user import user_bp
    from routes.password import password_bp
    from routes.media import media_bp
    from routes.auth import auth_bp
    from routes.main import main_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(password_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
