"""
Destiny MARC Builder

Program entry point.
"""

from __future__ import annotations

from config import load_settings


def main() -> int:
    settings = load_settings()

    print("Destiny MARC Builder")
    print()
    print("Settings loaded:")
    print(f"  Google API key: {'configured' if settings.google_api_key else 'not configured'}")
    print(f"  Lookup delay: {settings.lookup_delay}")
    print(f"  Timeout: {settings.timeout}")
    print(f"  Retry count: {settings.retry_count}")
    print(f"  Cache database: {settings.cache_database}")
    print(f"  Include Google link: {settings.include_google_link}")
    print(f"  Description length: {settings.description_length}")
    print(f"  Audit report: {settings.write_audit_report}")
    print(f"  Summary report: {settings.write_summary_report}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
