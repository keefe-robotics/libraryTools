"""
Google Books API client.
"""

from __future__ import annotations

import time
from typing import Any

import requests

from models import AppSettings, LookupResult


class GoogleBooksClient:
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"

    def __init__(self, settings: AppSettings):
        self.settings = settings

    def lookup(self, isbn: str) -> LookupResult:
        last_error = ""

        for attempt in range(1, self.settings.retry_count + 1):
            try:
                result = self._lookup_once(isbn)
                if self.settings.lookup_delay > 0:
                    time.sleep(self.settings.lookup_delay)
                return result
            except requests.RequestException as exc:
                last_error = str(exc)

                if attempt < self.settings.retry_count:
                    time.sleep(self.settings.lookup_delay * attempt)

        return LookupResult(
            isbn=isbn,
            status="error",
            source="google_books",
            error=last_error,
        )

    def _lookup_once(self, isbn: str) -> LookupResult:
        params: dict[str, Any] = {
            "q": f"isbn:{isbn}",
            "maxResults": 1,
            "printType": "books",
            "projection": "full",
        }

        if self.settings.google_api_key:
            params["key"] = self.settings.google_api_key

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=self.settings.timeout,
        )
        response.raise_for_status()

        data = response.json()
        items = data.get("items", [])

        if not items:
            return LookupResult(
                isbn=isbn,
                status="no_match",
                source="google_books",
                metadata={},
            )

        volume = items[0]
        volume_info = volume.get("volumeInfo", {})

        return LookupResult(
            isbn=isbn,
            status="matched",
            source="google_books",
            google_id=volume.get("id", ""),
            metadata=volume_info,
        )
