import hashlib
import json
import logging
from dataclasses import dataclass
from typing import Any, cast

from redis import Redis
from redis.exceptions import RedisError

from app.core.config import Settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CachedEmbedding:
    vector: list[float]


class EmbeddingCache:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        client_kwargs: dict[str, Any] = {"decode_responses": True}
        if settings.redis_password:
            client_kwargs["password"] = settings.redis_password
        self._client: Redis = Redis.from_url(settings.redis_url, **client_kwargs)

    def get(self, text: str, model: str) -> CachedEmbedding | None:
        key = self._key(text, model)
        try:
            raw_value = cast(str | bytes | bytearray | None, self._client.get(key))
        except RedisError as exc:
            logger.warning("Redis cache read failed for key=%s: %s", key, exc)
            return None

        if raw_value is None:
            return None

        try:
            payload = json.loads(raw_value)
            if not self._is_valid_payload(payload, text, model):
                logger.warning("Redis cache payload is invalid for key=%s", key)
                return None
            return CachedEmbedding(vector=[float(item) for item in payload["vector"]])
        except (TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
            logger.warning("Redis cache payload parsing failed for key=%s: %s", key, exc)
            return None

    def set(self, text: str, model: str, vector: list[float]) -> None:
        payload = {
            "text": text,
            "model": model,
            "vector": vector,
        }
        raw_value = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

        key = self._key(text, model)
        try:
            if self._settings.redis_cache_ttl_seconds > 0:
                self._client.setex(key, self._settings.redis_cache_ttl_seconds, raw_value)
            else:
                self._client.set(key, raw_value)
        except RedisError as exc:
            logger.warning("Redis cache write failed for key=%s: %s", key, exc)
            return

    def _key(self, text: str, model: str) -> str:
        digest = hashlib.sha256(f"{model}\0{text}".encode("utf-8")).hexdigest()
        return f"{self._settings.redis_key_prefix}:embedding:{digest}"

    @staticmethod
    def _is_valid_payload(payload: Any, text: str, model: str) -> bool:
        return (
            isinstance(payload, dict)
            and payload.get("text") == text
            and payload.get("model") == model
            and isinstance(payload.get("vector"), list)
            and len(payload["vector"]) > 0
        )
