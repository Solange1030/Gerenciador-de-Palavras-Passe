import secrets

def gen_otp():
    otp = secrets.randbelow(900000) + 100000
    return str(otp)

