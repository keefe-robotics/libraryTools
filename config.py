"""
Configuration loader.
"""

import configparser
from pathlib import Path


DEFAULT_SETTINGS_FILE = "settings.ini"


def load_settings(filename=DEFAULT_SETTINGS_FILE):
    config = configparser.ConfigParser()
    config.read(filename)
    return config
