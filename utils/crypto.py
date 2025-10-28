import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

FLASK_KEY = os.getenv("FLASK_KEY")

if not FLASK_KEY:
    raise ValueError("SECRET_KEY não encontrada! Define-a no .env ou nas variáveis do Render.")

if isinstance(FLASK_KEY, str):
    FLASK_KEY = FLASK_KEY.encode()

fernet = Fernet(FLASK_KEY)


def encrypt_value(value: str) -> bytes:
   
    return fernet.encrypt(value.encode())

def decrypt_value(token: bytes) -> str:

    return fernet.decrypt(token).decode()

