"""
Shared dataclasses for Destiny MARC Builder.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceRow:
    row_number: int
    copy_number: int
    isbn: str
    title: str = ""
    author: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class LookupResult:
    isbn: str
    status: str
    source: str = ""
    google_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str = ""


@dataclass
class AppSettings:
    google_api_key: str = ""
    lookup_delay: float = 0.5
    timeout: int = 20
    retry_count: int = 3
    cache_database: str = "google_books_cache.db"
    include_google_link: bool = False
    description_length: int = 500
    write_audit_report: bool = True
    write_summary_report: bool = True
