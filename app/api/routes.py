from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import get_settings
from app.models.schemas import SimilarityRequest, SimilarityResponse
from app.services.embedding import EmbeddingServiceError, OllamaEmbeddingService
from app.services.similarity import SimilarityService, TextRejectedError, VectorMathError

router = APIRouter()


@lru_cache
def get_similarity_service() -> SimilarityService:
    settings = get_settings()
    return SimilarityService(
        settings=settings,
        embedding_service=OllamaEmbeddingService(settings),
    )


@router.post(
    "/similarity",
    response_model=SimilarityResponse,
    summary="Calculate cosine similarity for two texts",
)
def calculate_similarity(
    request: SimilarityRequest,
    service: SimilarityService = Depends(get_similarity_service),
) -> SimilarityResponse:
    try:
        return service.compare(request.text1, request.text2)
    except TextRejectedError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except EmbeddingServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except VectorMathError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


@router.get("/health", summary="Backend health check")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "embeddingModel": settings.ollama_embedding_model,
    }
