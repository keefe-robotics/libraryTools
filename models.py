"""
Shared dataclasses.
"""

from dataclasses import dataclass


@dataclass
class Book:
    isbn: str = ""
