import os
from cryptography.fernet import Fernet

# Caminho absoluto do arquivo de chave
KEY_PATH = os.path.join(os.path.dirname(__file__), "../config/secret.key")

# Lê a chave existente
with open(KEY_PATH, "rb") as f:
    key = f.read()

fernet = Fernet(key)

def encrypt_value(value: str) -> bytes:
    
    return fernet.encrypt(value.encode())

def decrypt_value(token: bytes) -> str:
    print("teste")
    return fernet.decrypt(token).decode()
