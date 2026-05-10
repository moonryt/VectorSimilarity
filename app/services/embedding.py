from collections.abc import Sequence

from ollama import Client

from app.core.config import Settings


class EmbeddingServiceError(RuntimeError):
    pass


class OllamaEmbeddingService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        kwargs: dict[str, object] = {"timeout": settings.ollama_timeout_seconds}
        if settings.ollama_host:
            kwargs["host"] = settings.ollama_host
        self._client = Client(**kwargs)

    def embed(self, text: str) -> list[float]:
        try:
            response = self._client.embed(
                model=self._settings.ollama_embedding_model,
                input=text,
            )
        except Exception as exc:
            raise EmbeddingServiceError("文本嵌入服务不可用") from exc

        embeddings = getattr(response, "embeddings", None)
        if embeddings is None and isinstance(response, dict):
            embeddings = response.get("embeddings")

        if not isinstance(embeddings, Sequence) or not embeddings:
            raise EmbeddingServiceError("embedding service returned no vector")

        vector = embeddings[0]
        if not isinstance(vector, Sequence) or not vector:
            raise EmbeddingServiceError("embedding service returned an invalid vector")

        try:
            return [float(item) for item in vector]
        except (TypeError, ValueError) as exc:
            raise EmbeddingServiceError("embedding service returned non-numeric values") from exc

