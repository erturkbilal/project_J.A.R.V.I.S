from __future__ import annotations

import re

from langdetect import DetectorFactory, detect

DetectorFactory.seed = 0

LANGUAGE_HINTS: dict[str, str] = {
    "answer in english": "en",
    "speak english": "en",
    "ingilizce konuş": "en",
    "türkçe konuş": "tr",
    "turkce konus": "tr",
    "responde en español": "es",
    "réponds en français": "fr",
}


class LanguageService:
    def __init__(self) -> None:
        self._override_language: str | None = None

    @property
    def override_language(self) -> str | None:
        return self._override_language

    def resolve_language(self, text: str) -> str:
        override = self._extract_override(text)
        if override:
            self._override_language = override

        if self._override_language:
            return self._override_language

        try:
            return detect(text)
        except Exception:
            return "en"

    def _extract_override(self, text: str) -> str | None:
        normalized = re.sub(r"\s+", " ", text.lower()).strip()
        for phrase, lang in LANGUAGE_HINTS.items():
            if phrase in normalized:
                return lang
        return None
