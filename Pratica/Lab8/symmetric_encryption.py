from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from samples import SAMPLES
import os

def get_cipher(algo, key, iv=None):
    if algo == 'AES-128' or algo == 'AES-128-ECB':
        return Cipher(algorithms.AES(key), modes.ECB())
    if algo == 'AES-128-CBC':
        return Cipher(algorithms.AES128(key), modes.CBC(iv))
    
    return None

def generate_key(size=32):
    return os.urandom(size)

def generate_iv(size=16):
    return os.urandom(size)

def encrypt(key, iv, plaintext, cipher_name='AES-128-CBC'):
    cipher = get_cipher(cipher_name, key, iv)
    encryptor = cipher.encryptor()
    ct = encryptor.update(plaintext) + encryptor.finalize()
    return ct

def decrypt(key, iv, ciphertext, cipher_name='AES-128-CBC'):
    cipher = get_cipher(cipher_name, key, iv)
    decryptor = cipher.decryptor()
    pt = decryptor.update(ciphertext) + decryptor.finalize()
    return pt

def convert_hex_string_to_bytes(hex_string):
    return bytes.fromhex(hex_string)

def main():
    key = generate_key(16)
    iv = generate_iv(16)
    message = b"a secret message"

    ct = encrypt(key, iv, message)
    print(ct)

    pt = decrypt(key, iv, ct)
    print(pt)

    for i in SAMPLES:
        print(i['ALGO'])
        key = convert_hex_string_to_bytes(i['KEY'])
        plaintext = convert_hex_string_to_bytes(i['PLAINTEXT'])
        cyphertext = convert_hex_string_to_bytes(i['CIPHERTEXT'])

        iv = convert_hex_string_to_bytes(i['IV']) if 'IV' in i.keys() else None

        encrypt_message = encrypt(key, iv, plaintext, i['ALGO'])
        decrypt_message = decrypt(key, iv, cyphertext, i['ALGO'])

        if encrypt_message == cyphertext:
            print("Encrypt message matches expected cyphertext")
        if decrypt_message == plaintext:
            print("Decrypt message matches expected plaintext") 


def pad_data(data, block_size=128):
    padder = padding.PKCS7(block_size).padder()
    return padder.update(data) + padder.finalize()

def unpad_data(data, block_size=128):
    unpadder = padding.PKCS7(block_size).unpadder()
    return unpadder.update(data) + unpadder.finalize()

def padding_example():
    message = b'this is a secret message'

    key = generate_key(16)
    iv = generate_iv(16)

    padded_message = pad_data(message)
    encrypt_message = encrypt(key, iv, padded_message)
    unencrypted_message = decrypt(key, iv, encrypt_message)
    final_message = unpad_data(unencrypted_message).decode('utf-8')

    print("Encrypt message: ", final_message)


if __name__ == '__main__':
    main()
    padding_example()