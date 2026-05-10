import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SENSITIVE_WORDS_FILE = PROJECT_ROOT / "app" / "data" / "sensitive_words.txt"

load_dotenv(PROJECT_ROOT / ".env")


def _get_str(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip()


def _get_int(name: str, default: int, *, minimum: int | None = None) -> int:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value.strip() == "":
        return default
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be greater than or equal to {minimum}")
    return value


def _get_float(name: str, default: float, *, minimum: float | None = None) -> float:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value.strip() == "":
        return default
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number") from exc
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be greater than or equal to {minimum}")
    return value


def _get_csv(name: str, default: tuple[str, ...] = ()) -> tuple[str, ...]:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return tuple(item.strip() for item in raw_value.split(",") if item.strip())


def _resolve_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


@dataclass(frozen=True)
class Settings:
    app_name: str
    api_prefix: str
    cors_allowed_origins: tuple[str, ...]
    redis_url: str
    redis_password: str | None
    redis_key_prefix: str
    redis_cache_ttl_seconds: int
    ollama_host: str | None
    ollama_embedding_model: str
    ollama_timeout_seconds: float
    max_text_length: int
    sensitive_words: tuple[str, ...]
    sensitive_words_file: Path


@lru_cache
def get_settings() -> Settings:
    ollama_host = _get_str("OLLAMA_HOST", "")
    return Settings(
        app_name=_get_str("APP_NAME", "Vector Similarity API"),
        api_prefix=_get_str("API_PREFIX", "/api"),
        cors_allowed_origins=_get_csv(
            "CORS_ALLOWED_ORIGINS",
            (
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:3000",
                "http://127.0.0.1:3000",
            ),
        ),
        redis_url=_get_str("REDIS_URL", "redis://localhost:6379/0"),
        redis_password=_get_str("REDIS_PASSWORD", "") or None,
        redis_key_prefix=_get_str("REDIS_KEY_PREFIX", "vec"),
        redis_cache_ttl_seconds=_get_int("REDIS_CACHE_TTL_SECONDS", 86400, minimum=0),
        ollama_host=ollama_host or None,
        ollama_embedding_model=_get_str("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"),
        ollama_timeout_seconds=_get_float("OLLAMA_TIMEOUT_SECONDS", 30.0, minimum=0.1),
        max_text_length=_get_int("MAX_TEXT_LENGTH", 128, minimum=1),
        sensitive_words=_get_csv("SENSITIVE_WORDS"),
        sensitive_words_file=_resolve_path(
            _get_str("SENSITIVE_WORDS_FILE", str(DEFAULT_SENSITIVE_WORDS_FILE))
        ),
    )
