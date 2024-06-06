import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import secrets

def decrypt_file(file_path, key):
    backend = default_backend()
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    with open(file_path, 'wb') as f:
        f.write(decrypted_data)

def load_key():
    with open("schluessel.txt", "rb") as key_file:
        return key_file.read()

if __name__ == "__main__":
    # Name der zu entschlüsselnden ZIP-Datei
    zip_filename = "YouAreBusted.zip"

    # Lade den Schlüssel aus der Datei
    key = load_key()

    # Entschlüssele die ZIP-Datei
    decrypt_file(zip_filename, key)
    print(f"ZIP-Datei '{zip_filename}' wurde erfolgreich entschlüsselt.")
