from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(slots=True)
class Settings:
    openrouter_api_key: str
    openrouter_model: str
    app_db_path: Path
    encryption_key: str | None



def load_settings() -> Settings:
    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is required. Add it to your .env file.")

    db_path = Path(os.getenv("APP_DB_PATH", "data/jarvis.db"))
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return Settings(
        openrouter_api_key=api_key,
        openrouter_model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        app_db_path=db_path,
        encryption_key=os.getenv("ENCRYPTION_KEY") or None,
    )
