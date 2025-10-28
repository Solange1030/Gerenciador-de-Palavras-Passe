import base64
import time
from stegano import lsb
import os
from PIL import Image

#verificando se a imagem contem texto embutido
def has_hidden_message(img_path: str):
    try:
        password = lsb.reveal(img_path)
        if password is None:
            return False
        password = password.strip()
        return len(password) > 0
    except Exception as e:
        print(f"[DEBUG] Erro ao verificar palavra-passe oculta: {e}")
        return False

#embutir palavra-passe na imagem

def embed_pass_in_image(password: bytes, img_path):
   
    try:
        safe_token = base64.b64encode(password).decode()
        existing_password = lsb.reveal(img_path)
        if existing_password:
            raise ValueError("A imagem original já contém uma palavra-passe oculta.")
    except Exception:
        pass 
    img = Image.open(img_path)
    secret_image = lsb.hide(img, safe_token)
    

    return secret_image


#salvar imagem esteganofrada
def saving_stegno_file(filename, upload_folder, stego_image: Image.Image):

    stego_folder = os.path.join(upload_folder, "stego_files")
    os.makedirs(stego_folder, exist_ok=True)

    stego_filename = f"stego_{int(time.time())}_{os.path.splitext(filename)[0]}.png"
    final_path = os.path.join(stego_folder, stego_filename)
    print(final_path)
    stego_image.save(final_path, format="PNG")

    return final_path

def extrating_password(stego_path):
    try:
        msg = lsb.reveal(stego_path)
        if not msg:
            return False
        
        token_bytes = base64.b64decode(msg.encode())
        return token_bytes
    except Exception as e:
        print(f"Erro ao extrair mensagem: {e}")
        return False

