from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"


def _parse_env_line(line: str) -> Optional[tuple[str, str]]:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if "=" not in line:
        return None
    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip().strip('"').strip("'")
    if not key:
        return None
    return key, value


def load_env(path: Optional[Path] = None) -> None:
    env_path = path or ENV_PATH
    if not env_path.exists():
        return
    try:
        content = env_path.read_text(encoding="utf-8")
    except OSError:
        return
    for line in content.splitlines():
        parsed = _parse_env_line(line)
        if not parsed:
            continue
        key, value = parsed
        if key not in os.environ:
            os.environ[key] = value


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(name, default)


class Settings:
    def __init__(self) -> None:
        load_env()
        self.app_name = get_env("APP_NAME", "Study Planner API")
        self.jwt_secret = get_env("JWT_SECRET", "change_me")
        self.jwt_expires_minutes = int(get_env("JWT_EXPIRES_MINUTES", "60") or 60)
        self.db_path = str(BASE_DIR / "database" / "database.db")
        cors = get_env("CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501")
        self.cors_origins = [c.strip() for c in cors.split(",") if c.strip()]
        self.log_level = get_env("LOG_LEVEL", "INFO")
