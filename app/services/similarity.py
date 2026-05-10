import math
import uuid
from datetime import UTC, datetime

import numpy as np

from app.core.config import Settings
from app.models.schemas import SanitizedTexts, SimilarityResponse
from app.services.cache import EmbeddingCache
from app.services.embedding import OllamaEmbeddingService
from app.services.sensitive_words import SensitiveWordMatcher


class TextRejectedError(ValueError):
    pass


class VectorMathError(RuntimeError):
    pass


class SimilarityService:
    def __init__(
        self,
        settings: Settings,
        embedding_service: OllamaEmbeddingService,
    ) -> None:
        self._settings = settings
        self._embedding_service = embedding_service
        self._cache = EmbeddingCache(settings)
        self._sensitive_words = SensitiveWordMatcher(settings)

    def compare(self, text1: str, text2: str) -> SimilarityResponse:
        self._validate_text(text1)
        self._validate_text(text2)

        if text1 == text2:
            return self._build_response(
                text1=text1,
                text2=text2,
                cosine=1.0,
                adjusted_percent=100.0,
            )

        vector1 = self._get_embedding(text1)
        vector2 = self._get_embedding(text2)
        cosine = self._cosine_similarity(vector1, vector2)
        return self._build_response(text1=text1, text2=text2, cosine=cosine)

    def _build_response(
        self,
        text1: str,
        text2: str,
        cosine: float,
        adjusted_percent: float | None = None,
    ) -> SimilarityResponse:
        percent_value = round(cosine * 100, 2)
        if adjusted_percent is None:
            adjusted_percent = self._adjusted_percent(cosine)

        return SimilarityResponse(
            id=uuid.uuid4().hex[:12],
            completedAt=datetime.now(UTC).isoformat(),
            cosine=cosine,
            cosineFullPrecision=format(cosine, ".17g"),
            percent=f"{percent_value:.2f}%",
            percentValue=percent_value,
            adjustedPercent=f"{adjusted_percent:.2f}%",
            adjustedValue=round(adjusted_percent, 2),
            model=self._settings.ollama_embedding_model,
            texts=SanitizedTexts(text1=text1, text2=text2),
        )

    def _validate_text(self, text: str) -> None:
        if len(text) > self._settings.max_text_length:
            raise TextRejectedError(
                f"文本长度需要小于等于 {self._settings.max_text_length}"
            )
        if self._sensitive_words.contains_sensitive_word(text):
            raise TextRejectedError("文本包含敏感词")

    def _get_embedding(self, text: str) -> list[float]:
        model = self._settings.ollama_embedding_model
        cached_embedding = self._cache.get(text, model)
        if cached_embedding is not None:
            return cached_embedding.vector

        vector = self._embedding_service.embed(text)
        self._cache.set(text, model, vector)
        return vector

    @staticmethod
    def _adjusted_percent(cosine: float) -> float:
        normalized = (cosine + 1.0) / 2.0
        sigmoid = 1.0 / (1.0 + math.exp(-8.0 * (normalized - 0.65)))
        return (sigmoid**0.8) * 100.0

    @staticmethod
    def _cosine_similarity(vector1: list[float], vector2: list[float]) -> float:
        if len(vector1) != len(vector2):
            raise VectorMathError("embedding vectors must have the same dimensions")

        left = np.asarray(vector1, dtype=np.float64)
        right = np.asarray(vector2, dtype=np.float64)

        left_norm = np.linalg.norm(left)
        right_norm = np.linalg.norm(right)
        denominator = left_norm * right_norm
        if denominator == 0 or not math.isfinite(float(denominator)):
            raise VectorMathError("embedding vector norm must be finite and non-zero")

        cosine = float(np.dot(left, right) / denominator)
        if not math.isfinite(cosine):
            raise VectorMathError("cosine similarity must be finite")
        return cosine
