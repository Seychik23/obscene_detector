# Copyright (c) 2025 Seychik23
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import os
import configparser
from cryptography.fernet import Fernet
from pathlib import Path

from .conf_manager import get_language, get_encryption_key, PROJECT_ROOT


def _decrypt_words(filepath: str, key: bytes) -> list:
    try:
        f = Fernet(key)
        with open(filepath, 'rb') as file:
            encrypted_data = file.read()
        
        decrypted_data = f.decrypt(encrypted_data).decode('utf-8')
        words = decrypted_data.split("|||")
        return [word.lower() for word in words if word]
    except FileNotFoundError:
        print(f"ERROR: Word list file not found: {filepath}")
        print("Please make sure you have created it using the encrypt_words.py script")
        return []
    except Exception as e:
        print(f"ERROR: Could not decrypt {filepath}. Is the key correct? Error: {e}")
        return []
    

def load_words_for_current_language() -> list:
    """
    Main function. Loads the config, determines the language, and returns
    the decrypted list of words for that language.
    """
    language =  get_language()
    encryption_key = get_encryption_key()

    if not language or not encryption_key:
        return []

    data_file_path = PROJECT_ROOT / 'data' / f'bad_words_{language.upper()}.dat'

    return _decrypt_words(str(data_file_path), encryption_key)
