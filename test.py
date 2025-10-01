from app import db, create_app
from controllers.PasswordController import create_password
from controllers.user_controller import create_user

app = create_app()
with app.app_context():
    create_password("licha", "pessoal", "hsbdcdbchjcbh", "Google", "https//google.com", "solangemaria@gmail.com")
    # create_user("Solange Maria", "solangemaria@gmail.com", "Solange")
    print("Dados registada")