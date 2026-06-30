"""
Destiny MARC Builder

Program entry point.
"""

from __future__ import annotations

import sys

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

    print("Destiny MARC Builder")
    print()
    print(f"Input file: {input_file}")
    print(f"ISBN entries found: {len(rows)}")
    print(f"Unique ISBNs: {len(unique_isbns)}")
    print(f"Google API key: {'configured' if settings.google_api_key else 'not configured'}")

    print()
    print("First 10 ISBNs:")
    for row in rows[:10]:
        print(f"  row {row.row_number}: {row.isbn}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
