"""
Destiny MARC Builder

Program entry point.
"""

from __future__ import annotations
from version import __version__

import sys
import platform
from collections import Counter

from cache import Cache
from config import load_settings
from excel_reader import ExcelReader
from google_books import GoogleBooksClient


def main() -> int:
    settings = load_settings()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py input.xlsx")
        print("  python main.py isbn_list.txt")
        print("  python main.py isbn_list.csv")
        return 1

    input_file = sys.argv[1]

    reader = ExcelReader()
    rows = reader.read(input_file)

    unique_isbns = sorted({row.isbn for row in rows})
    isbn_counts = Counter(row.isbn for row in rows)

    duplicate_copy_count = sum(count - 1 for count in isbn_counts.values() if count > 1)

    cache = Cache(settings.cache_database)
    google = GoogleBooksClient(settings)

    cached_count = 0
    looked_up_count = 0
    matched_count = 0
    no_match_count = 0
    error_count = 0

    print(f"Destiny MARC Builder v{__version__}")
    print(f"Python {platform.python_version()}")
    print()
    print(f"Input file: {input_file}")
    print(f"ISBN entries found: {len(rows)}")
    print(f"Unique ISBNs: {len(unique_isbns)}")
    print(f"Duplicate copies: {duplicate_copy_count}")
    print()
    print(f"Google API key: {'configured' if settings.google_api_key else 'not configured'}")
    print(f"Cache database: {settings.cache_database}")
    print(f"Cached ISBNs in database before run: {cache.count()}")
    print()
    print("Looking up uncached ISBNs...")
    print()

    for index, isbn in enumerate(unique_isbns, start=1):
        cached = cache.get(isbn)

        if cached:
            cached_count += 1
            result = cached
            source_label = f"{result.source}_cached"
        else:
            result = google.lookup(isbn)
            cache.set(result)
            looked_up_count += 1
            source_label = result.source

        if result.status == "matched":
            matched_count += 1
        elif result.status == "no_match":
            no_match_count += 1
        else:
            error_count += 1

        print(
            f"[{index}/{len(unique_isbns)}] "
            f"ISBN {isbn}: {source_label} / {result.status}"
        )

    print()
    print("Lookup summary:")
    print(f"  Input ISBN entries: {len(rows)}")
    print(f"  Unique ISBNs: {len(unique_isbns)}")
    print(f"  Duplicate copies: {duplicate_copy_count}")
    print(f"  Already cached: {cached_count}")
    print(f"  Looked up now: {looked_up_count}")
    print(f"  Matched: {matched_count}")
    print(f"  No match: {no_match_count}")
    print(f"  Errors: {error_count}")
    print(f"  Cache database total: {cache.count()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
