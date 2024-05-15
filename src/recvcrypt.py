from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

app = Flask(__name__)

def decrypt_data(encrypted_data_hex, key):
    cipher = AESCipher(key)
    encrypted_data = base64.b64decode(encrypted_data_hex)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

class AESCipher:
    def __init__(self, key):
        self.key = key
        self.cipher = AES.new(self.key, AES.MODE_ECB)
    def decrypt(self, ciphertext):
        decrypted = self.cipher.decrypt(ciphertext)
        return decrypted
    
@app.route ('/decrypt', methods=['POST'])            
def decrypt():
    key = b'1234567891234567'
    encrypted_data_hex = request.json.get('encrypted_data')
    if encrypted_data_hex:
        try:
            decrypted_data = decrypt_data(encrypted_data_hex, key)
            return jsonify({'decrypted_data': decrypted_data.hex()}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else: 
         return jsonify({'error': 'Encrypted data not provided'}), 400
    
if __name__ == "__main__":
     app.run(host = '0.0.0.0', port=5000, debug=True)
