from typing import Dict
from ..locales.language_data import SUPPORTED_LANGUAGES


def show_results(result: Dict, language: str = "tr-TR"):
    lang_name = SUPPORTED_LANGUAGES.get(language, {}).get("native", language)

    print(f"\n{lang_name} Değerlendirme Sonuçları:")
    print(f"Puan: {result['score']:.1f}/100")
    print(f"Doğruluk: {result['accuracy']:.1f}%")

    if result['errors']:
        print(f"\nDüzeltilmesi gerekenler: {', '.join(result['errors'])}")