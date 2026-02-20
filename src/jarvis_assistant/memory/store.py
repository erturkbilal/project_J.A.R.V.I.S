from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(slots=True)
class MemoryStore:
    db_path: Path

    def __post_init__(self) -> None:
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    language TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS learned_commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT NOT NULL,
                    hit_count INTEGER NOT NULL DEFAULT 1,
                    last_used_at TEXT NOT NULL
                );
                """
            )

    def save_message(self, role: str, content: str, language: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO conversations(role, content, language, created_at) VALUES (?, ?, ?, ?)",
                (role, content, language, timestamp),
            )

    def recent_messages(self, limit: int = 12) -> list[dict[str, str]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()

        history = [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]
        return history

    def set_preference(self, key: str, value: dict | str) -> None:
        serialized = value if isinstance(value, str) else json.dumps(value)
        timestamp = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO user_preferences(key, value, updated_at) VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
                """,
                (key, serialized, timestamp),
            )

    def get_preference(self, key: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM user_preferences WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    def remember_command(self, command_text: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT id, hit_count FROM learned_commands WHERE command = ?", (command_text,)
            ).fetchone()
            if existing:
                conn.execute(
                    "UPDATE learned_commands SET hit_count = ?, last_used_at = ? WHERE id = ?",
                    (existing["hit_count"] + 1, timestamp, existing["id"]),
                )
            else:
                conn.execute(
                    "INSERT INTO learned_commands(command, hit_count, last_used_at) VALUES (?, ?, ?)",
                    (command_text, 1, timestamp),
                )
