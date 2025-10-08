from cryptography.fernet import Fernet
import os

key_path = os.path.join(os.path.dirname(__file__), "config", "secret.key")

os.makedirs(os.path.dirname(key_path), exist_ok=True)

key = Fernet.generate_key()
with open(key_path, "wb") as f:
    f.write(key)

print("Chave Fernet gerada e salva em {key_path}")
