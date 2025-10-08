from app import db, create_app
from controllers.password_controller import create_password
from controllers.auth_controller import sign_up

app = create_app()
with app.app_context():
    data ={
        "name" : "Solange Maria",
        "email" : "solangemaria@gmail.com"
    }
    sign_up( data)
    print("Dados registada")

