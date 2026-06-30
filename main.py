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

    cached_count = 0
    uncached_count = 0

    for isbn in unique_isbns:
        if cache.get(isbn):
            cached_count += 1
        else:
            uncached_count += 1

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
    print(f"Cached ISBNs in database: {cache.count()}")
    print(f"Input ISBNs already cached: {cached_count}")
    print(f"Input ISBNs needing lookup: {uncached_count}")

    print()
    print("First 10 ISBN entries:")
    for row in rows[:10]:
        print(f"  row {row.row_number}: {row.isbn}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
