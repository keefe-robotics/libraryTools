# Architecture

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
