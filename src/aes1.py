import cryptolib

key = b'1234567812345678'

mode = 1

aes_encrypt = cryptolib.aes(key, mode)
aes_decrypt = cryptolib.aes(key, mode)

data = 'thisisData'
data_bytes = data.encode()

block_size = 16
padding_length = block_size - (len(data_bytes) % block_size)
padded_data = data_bytes + bytes([padding_length] * padding_length)

encrypted_data = aes_encrypt.encrypt(padded_data)

print("Encrypted data (hex):", encrypted_data.hex())

decrypted_data = aes_decrypt.decrypt(encrypted_data).rstrip(b'\x00').decode()

print("original data", data)
print("decrypted data", decrypted_data)

