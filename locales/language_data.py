# -*- coding: utf-8 -*-
"""
Supported languages and their metadata based on Azure Speech Service capabilities
"""

SUPPORTED_LANGUAGES = {
    "en-US": {
        "name": "English (US)",
        "native_name": "English (United States)",
        "voice": "en-US-JennyNeural",
        "phoneme_alphabet": "IPA",
        "text_to_speech": True,
        "pronunciation_assessment": True
    },
    "tr-TR": {
        "name": "Turkish",
        "native_name": "Türkçe",
        "voice": "tr-TR-AhmetNeural",
        "phoneme_alphabet": "IPA",
        "text_to_speech": True,
        "pronunciation_assessment": True
    },
    "de-DE": {
        "name": "German",
        "native_name": "Deutsch",
        "voice": "de-DE-ConradNeural",
        "phoneme_alphabet": "IPA",
        "text_to_speech": True,
        "pronunciation_assessment": True
    }
    # Diğer diller eklenebilir
}


def get_language_name(language_code: str, native: bool = False) -> str:
    """
    Get display name for a language code

    Args:
        language_code: ISO language code (e.g. 'en-US')
        native: Whether to return native name

    Returns:
        Display name of the language
    """
    lang = SUPPORTED_LANGUAGES.get(language_code)
    if not lang:
        raise ValueError(f"Unsupported language code: {language_code}")

    return lang["native_name"] if native else lang["name"]


def get_supported_locales(feature: str = "pronunciation_assessment") -> list:
    """
    Get list of supported locales for specific feature

    Args:
        feature: Feature type ('pronunciation_assessment' or 'text_to_speech')

    Returns:
        List of supported locale codes
    """
    return [
        code for code, meta in SUPPORTED_LANGUAGES.items()
        if meta.get(feature, False)
    ]