from typing import Dict, List, Optional
from pathlib import Path
import json

from ..config.settings import settings
from ..utils.logger import logger
from .exceptions import LanguageNotSupportedError
from ..locales.language_data import SUPPORTED_LANGUAGES


class LanguageManager:
    def __init__(self):
        self.supported_languages = SUPPORTED_LANGUAGES
        self.translations = self._load_translations()
        logger.info("Language Manager initialized")

    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translation files from locales directory"""
        translations = {}
        locales_dir = Path(__file__).parent.parent.parent / "locales" / "translations"

        for lang_file in locales_dir.glob("*.json"):
            lang_code = lang_file.stem
            with open(lang_file, 'r', encoding='utf-8') as f:
                translations[lang_code] = json.load(f)

        return translations

    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages with metadata"""
        return [
            {
                "code": code,
                "name": meta["name"],
                "native_name": meta["native_name"]
            }
            for code, meta in self.supported_languages.items()
        ]

    def validate_language(self, language_code: str) -> bool:
        """Check if language is supported"""
        return language_code in self.supported_languages

    def get_translation(self, language_code: str, key: str) -> Optional[str]:
        """Get translation for a specific key"""
        if not self.validate_language(language_code):
            raise LanguageNotSupportedError(f"Language not supported: {language_code}")

        return self.translations.get(language_code, {}).get(key)

    def get_language_metadata(self, language_code: str) -> Dict[str, str]:
        """Get metadata for a specific language"""
        if not self.validate_language(language_code):
            raise LanguageNotSupportedError(f"Language not supported: {language_code}")

        return self.supported_languages[language_code]