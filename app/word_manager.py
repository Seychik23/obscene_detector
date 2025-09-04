# Copyright (c) 2025 Seychik23
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import os
import configparser
from cryptography.fernet import Fernet
from pathlib import Path

CONFIG_FILE = 'detector.conf'

# def _create_default_config():

def load_config():
    # Loads the configuration from a file. Creates it if it is missing.
    if not os.path.exists(CONFIG_FILE):
        return(f'Config not found!') #create_default_config()
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    return config

# def _create_default_config()

def load_words_for_current_language() -> list:
    """
    Main function. Loads the config, determines the language, and returns
    the decrypted list of words for that language.
    """
    config = load_config()

    if isinstance(config, str):
        print(config) 
        return []
    
    try:
        language = config.get('Settings', 'language')
        key_str = config.get('Settings', 'encryption_key')
        encryption_key = key_str.encode('ascii')
        f = Fernet(encryption_key) 
    
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"ERROR: Configuration file {CONFIG_FILE} is corrupt or incomplete. {e}")
        return []
    
    current_file_path = Path(__file__).resolve()

    project_root = current_file_path.parents[1]

    data_file_path = project_root / 'data' / f'bad_words_{language.upper()}.dat'
    
    print(f"Loading word list for language: {language.upper()}")


    return _decrypt_words(str(data_file_path), encryption_key)


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
''' 
def lload_words_for_current_language(filename='bad_words.dat'):
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
'''