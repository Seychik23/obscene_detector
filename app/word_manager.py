# Copyright (c) 2025 Seychik23
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import os
from cryptography.fernet import Fernet

KEY = b''  # for testing only

'''
# Load key from .conf
def load_encryption_key(config_file='oscene_detector.conf'):
    try:
        with open(config_file, 'r') as file:
            for line in file:
                if line.startswith('encryption_key='):
                    return line.split('=')[1].strip().encode()  
    except Exception as e:
        print(f"Error loading encryption key: {e}")
        return None

# Multilang support
def load_bad_words(language='RU'):
    filename = f'bad_words{language}.dat' 
    try:
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            return []

'''

def load_bad_words(filename='bad_words.dat'):
    try:
        f = Fernet(KEY)
        with open(filename, 'rb') as file:
            encrypted_data = file.read()
            
        decrypted_data = f.decrypt(encrypted_data).decode('utf-8')
        words = decrypted_data.split("|||")
        return [word.lower() for word in words]
    except Exception as e:
        print(f"Error while loading words list: {e}")
        return []
