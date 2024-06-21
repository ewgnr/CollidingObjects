import rncryptor, os
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = os.getenv("SECRET")
ALGORITHM = "HS256"

class Authorization:
    def __init__(self):
        self.cryptor = rncryptor.RNCryptor()

    def authenticate_user(self, hash, username, password):
        try:
            user = self.cryptor.decrypt(bytes.fromhex(hash), password)
            if user == username:
                return user
            else:
                return False
        except:
            return False

    def create_access_token(self, data):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=1440)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
