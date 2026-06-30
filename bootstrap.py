#!/usr/bin/env python3
"""
Bootstrap the Destiny MARC Builder project.

Run once from the root of an empty git repository.

    python bootstrap_project.py
"""

from pathlib import Path


FILES = {
    "main.py": '''"""
Destiny MARC Builder

Program entry point.
"""

from config import load_settings


def main():
    settings = load_settings()
    print("Destiny MARC Builder")
    print(settings)


if __name__ == "__main__":
    main()
''',

    "config.py": '''"""
Configuration loader.
"""

import configparser
from pathlib import Path


DEFAULT_SETTINGS_FILE = "settings.ini"


def load_settings(filename=DEFAULT_SETTINGS_FILE):
    config = configparser.ConfigParser()
    config.read(filename)
    return config
''',

    "excel_reader.py": '''"""
Read Excel and CSV files.
"""


class ExcelReader:
    pass
''',

    "google_books.py": '''"""
Google Books API interface.
"""


class GoogleBooksClient:
    pass
''',

    "marc_builder.py": '''"""
Build MARC21 records.
"""


class MarcBuilder:
    pass
''',

    "report_writer.py": '''"""
Generate audit and summary reports.
"""


class ReportWriter:
    pass
''',

    "cache.py": '''"""
SQLite cache.
"""


class Cache:
    pass
''',

    "isbn.py": '''"""
ISBN utilities.
"""


def normalize(isbn: str) -> str:
    return isbn
''',

    "models.py": '''"""
Shared dataclasses.
"""

from dataclasses import dataclass


@dataclass
class Book:
    isbn: str = ""
''',

    "requirements.txt": '''openpyxl
pymarc
requests
''',

    ".gitignore": '''__pycache__/
*.pyc
*.pyo

*.db
*.sqlite
*.sqlite3

*.mrc
*.mrk

*.csv

google_books_cache.*

.vscode/
.idea/

.env
''',

    "README.md": '''# Destiny MARC Builder

Build Destiny-compatible MARC21 records from Excel spreadsheets using Google Books and other metadata sources.

## Status

Early development.
''',

    "ARCHITECTURE.md": '''# Architecture

## Modules

main.py
    Application entry point

config.py
    Reads settings.ini

excel_reader.py
    Reads Excel input

google_books.py
    Google Books API

cache.py
    SQLite metadata cache

isbn.py
    ISBN conversion and validation

marc_builder.py
    Creates MARC21 records

report_writer.py
    Generates reports

models.py
    Shared dataclasses
''',

    "LICENSE": '''MIT License

Copyright (c) 2026
''',

    "settings.ini": '''[google]
api_key=

[lookup]
delay=0.5
timeout=20
retry_count=3

[cache]
database=google_books_cache.db

[marc]
include_google_link=false
description_length=500

[reports]
audit=true
summary=true
'''
}


def main():

    print()

    for filename, contents in FILES.items():
        path = Path(filename)

        if path.exists():
            print(f"Skipping {filename}")
            continue

        path.write_text(contents.strip() + "\n", encoding="utf-8")
        print(f"Created {filename}")

    print()
    print("Project bootstrapped successfully.")


if __name__ == "__main__":
    main()