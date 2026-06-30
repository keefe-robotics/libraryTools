"""
Configuration loader.
"""

from __future__ import annotations

import configparser
import os
from pathlib import Path

from models import AppSettings


DEFAULT_SETTINGS_FILE = "settings.ini"
DEFAULT_API_KEY_FILE = "google_books_api_key.txt"


def _get_bool(config: configparser.ConfigParser, section: str, option: str, default: bool) -> bool:
    if not config.has_option(section, option):
        return default
    return config.getboolean(section, option)


def _get_float(config: configparser.ConfigParser, section: str, option: str, default: float) -> float:
    if not config.has_option(section, option):
        return default
    return config.getfloat(section, option)


def _get_int(config: configparser.ConfigParser, section: str, option: str, default: int) -> int:
    if not config.has_option(section, option):
        return default
    return config.getint(section, option)


def _get_str(config: configparser.ConfigParser, section: str, option: str, default: str) -> str:
    if not config.has_option(section, option):
        return default
    return config.get(section, option).strip()


def load_api_key(config_key: str = "") -> str:
    if config_key:
        return config_key.strip()

    env_key = os.getenv("GOOGLE_BOOKS_API_KEY", "").strip()
    if env_key:
        return env_key

    key_file = Path(DEFAULT_API_KEY_FILE)
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()

    return ""


def load_settings(filename: str = DEFAULT_SETTINGS_FILE) -> AppSettings:
    config = configparser.ConfigParser()
    config.read(filename)

    config_api_key = _get_str(config, "google", "api_key", "")

    return AppSettings(
        google_api_key=load_api_key(config_api_key),
        lookup_delay=_get_float(config, "lookup", "delay", 0.5),
        timeout=_get_int(config, "lookup", "timeout", 20),
        retry_count=_get_int(config, "lookup", "retry_count", 3),
        cache_database=_get_str(config, "cache", "database", "google_books_cache.db"),
        include_google_link=_get_bool(config, "marc", "include_google_link", False),
        description_length=_get_int(config, "marc", "description_length", 500),
        write_audit_report=_get_bool(config, "reports", "audit", True),
        write_summary_report=_get_bool(config, "reports", "summary", True),
    )
