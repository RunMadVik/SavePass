import jwt
from cryptography.fernet import Fernet
from hashlib import sha256

def generate_token(user):
    
    payload = {
        "id": (user.uuid).hex
    }

    token = jwt.encode(payload, 'pass_secret',
                        algorithm="HS256")
    
    return token

def generate_key():
    key = Fernet.generate_key()
    return key.decode('utf-8')

def generate_hash(key):
        hash = sha256(key.encode('utf-8'))
        return hash.hexdigest()