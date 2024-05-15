import ucryptolib as cryptolib
import urequests

class Encryptor:
    def __init__(self, key, mode):
        self.key = key
        self.mode = mode
        self.aes = cryptolib.aes(key, mode)
        
    def encrypt_data(self, data):
        data_bytes = data.encode()
        block_size = 16
        padding_length = block_size - (len(data_bytes) % block_size)
        padded_data = data_bytes + bytes([padding_length] * padding_length)
        encrypted_data = self.aes.encrypt(padded_data)
        return encrypted_data.hex()
        
class Sender:
    def __init__(self, url):
        self.url = url
    
    def send_encrypted_data(self, encrypted_data_hex):
        headers = {'Content-Type': 'application/json'}
        payload = {'encrypted_data': encrypted_data_hex}
        response = urequests.post(self.url, json=payload, headers=headers)
        return response.text
    
# Krypteringsparametre
if __name__ == "__main__":
    
    key = b'1234567891234567'
    mode = 1

    encryptor = Encryptor(key, mode)

    sender = Sender('http://192.168.99.145:5000/decrypt')

    data = '1337'
    
    block_size = 16
    padding_length = block_size - (len(data) % block_size)
    padded_data = data + chr(padding_length) * padding_length
    
    encrypted_data_hex = encryptor.encrypt_data(padded_data)

    response = sender.send_encrypted_data(encrypted_data_hex)

    print("Response", response)

