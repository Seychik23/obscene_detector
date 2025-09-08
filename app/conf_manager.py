# Copyright (c) 2025 Seychik23
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import configparser

from pathlib import Path
from cryptography.fernet import Fernet

# Constants and paths
CONFIG_FILE = 'detector.conf'

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE_PATH = PROJECT_ROOT / CONFIG_FILE

def _load_config()-> configparser.ConfigParser:
    """ Loads the configuration from a file. Creates it if it is missing."""
    if not CONFIG_FILE_PATH.exists():
        print(f"Config file not found at {CONFIG_FILE_PATH}!")
        return _create_default_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    return config

def _create_default_config() -> configparser.ConfigParser:
    """Creates a default detector.conf with a new encryption key."""
    config = configparser.ConfigParser()
    config['Settings'] = {}
    
    print(f"File '{CONFIG_FILE}' not found. Creating a new default config...")
    
    new_key = Fernet.generate_key()
    
    config['Settings']['language'] = 'RU'
    config['Settings']['encryption_key'] = new_key.decode('utf-8')
    
    with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    print(f"New encryption key generated and saved to {CONFIG_FILE_PATH}")
    
    return config


config = _load_config()


def get_language() -> str | None:
    """Gets the language setting from the config."""
    try:
        return config.get('Settings', 'language')
    except (configparser.NoSectionError, configparser.NoOptionError):
        print("ERROR: 'language' not found in config file.")
        return None

def get_encryption_key() -> bytes | None:
    """Gets and decodes the encryption key from the config."""
    try:
        key_str = config.get('Settings', 'encryption_key')
        return key_str.encode('utf-8')
    except (configparser.NoSectionError, configparser.NoOptionError):
        print("ERROR: 'encryption_key' not found in config file.")
        return None





