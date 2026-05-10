import unicodedata

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator


def _contains_control_character(value: str) -> bool:
    return any(unicodedata.category(char) in {"Cc", "Cs"} for char in value)


class SimilarityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    text1: str = Field(
        strict=True,
        min_length=1,
        validation_alias=AliasChoices("text1", "word1", "left"),
    )
    text2: str = Field(
        strict=True,
        min_length=1,
        validation_alias=AliasChoices("text2", "word2", "right"),
    )

    @field_validator("text1", "text2")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("text must not be empty after trimming")
        if _contains_control_character(trimmed):
            raise ValueError("text must not contain control characters")
        return trimmed


class SanitizedTexts(BaseModel):
    text1: str
    text2: str


class SimilarityResponse(BaseModel):
    id: str
    completedAt: str
    cosine: float
    cosineFullPrecision: str
    percent: str
    percentValue: float
    adjustedPercent: str
    adjustedValue: float
    model: str
    texts: SanitizedTexts
