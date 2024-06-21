import rncryptor

class Crypto:
    def __init__(self):
        self.cryptor = rncryptor.RNCryptor()

    def encrypt(self, data:str, password:str):
        encrypted_data = self.cryptor.encrypt(data, password).hex()
        return encrypted_data

    def decrypt(self, data:str, password:str):
        decrypted_data = self.cryptor.decrypt(bytes.fromhex(data), password)
        return decrypted_data