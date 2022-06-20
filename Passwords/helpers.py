from cryptography.fernet import Fernet

def encrypt_password(password, key):
    f = Fernet(key.encode('utf-8'))
    e_pass = f.encrypt(password.encode('utf-8'))
    return e_pass.decode('utf-8')

def decrypt_password(key, password):
    key = key.encode('utf-8')
    f= Fernet(key)
    password = password.encode('utf-8')
    d_pass = f.decrypt(password)
    return d_pass