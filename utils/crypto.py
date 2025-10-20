import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY não encontrada! Define-a no .env ou nas variáveis do Render.")


if isinstance(SECRET_KEY, str):
    SECRET_KEY = SECRET_KEY.encode()

fernet = Fernet(SECRET_KEY)

def encrypt_value(value: str) -> bytes:
   
    return fernet.encrypt(value.encode())

def decrypt_value(token: bytes) -> str:

    return fernet.decrypt(token).decode()
