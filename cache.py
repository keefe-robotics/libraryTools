"""
SQLite cache for metadata lookups.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from models import LookupResult


class Cache:
    def __init__(self, database: str | Path):
        self.database = Path(database)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS lookup_cache (
                    isbn TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    source TEXT NOT NULL,
                    google_id TEXT NOT NULL DEFAULT '',
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    error TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def get(self, isbn: str) -> LookupResult | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT isbn, status, source, google_id, metadata_json, error
                FROM lookup_cache
                WHERE isbn = ?
                """,
                (isbn,),
            ).fetchone()

        if row is None:
            return None

        return LookupResult(
            isbn=row["isbn"],
            status=row["status"],
            source=row["source"],
            google_id=row["google_id"],
            metadata=json.loads(row["metadata_json"] or "{}"),
            error=row["error"],
        )

    def set(self, result: LookupResult) -> None:
        now = datetime.now(timezone.utc).isoformat()

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO lookup_cache (
                    isbn,
                    status,
                    source,
                    google_id,
                    metadata_json,
                    error,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(isbn) DO UPDATE SET
                    status = excluded.status,
                    source = excluded.source,
                    google_id = excluded.google_id,
                    metadata_json = excluded.metadata_json,
                    error = excluded.error,
                    updated_at = excluded.updated_at
                """,
                (
                    result.isbn,
                    result.status,
                    result.source,
                    result.google_id,
                    json.dumps(result.metadata, ensure_ascii=False),
                    result.error,
                    now,
                    now,
                ),
            )

    def count(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS count FROM lookup_cache").fetchone()
        return int(row["count"])

    def clear(self) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM lookup_cache")
