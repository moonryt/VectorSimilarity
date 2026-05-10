import unicodedata

from app.core.config import Settings


class SensitiveWordMatcher:
    def __init__(self, settings: Settings) -> None:
        self._words = self._load_words(settings)

    def contains_sensitive_word(self, text: str) -> bool:
        normalized_text = self._normalize(text)
        return any(word in normalized_text for word in self._words)

    @classmethod
    def _load_words(cls, settings: Settings) -> tuple[str, ...]:
        words: set[str] = set()

        for word in settings.sensitive_words:
            normalized = cls._normalize(word.strip())
            if normalized:
                words.add(normalized)

        if settings.sensitive_words_file.exists():
            file_content = settings.sensitive_words_file.read_text(encoding="utf-8")
            for line in file_content.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                normalized = cls._normalize(stripped)
                if normalized:
                    words.add(normalized)

        return tuple(sorted(words, key=len, reverse=True))

    @staticmethod
    def _normalize(value: str) -> str:
        return unicodedata.normalize("NFKC", value)
