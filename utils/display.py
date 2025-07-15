from typing import Dict
from ..models.assessment_result import PronunciationAssessmentResult
from ..locales.language_data import SUPPORTED_LANGUAGES


def show_results(result: PronunciationAssessmentResult, language: str = "tr-TR"):
    lang_name = SUPPORTED_LANGUAGES.get(language, {}).get("native", language)

    print(f"\n{lang_name} Değerlendirme Sonuçları:")
    print(f"Puan: {result.pron_score:.1f}/100")
    print(f"Doğruluk: {result.accuracy_score:.1f}%")
    print(f"Akıcılık: {result.fluency_score:.1f}")
    print(f"Tamlık: {result.completeness_score:.1f}")

    for word in result.words:
        print(f" - {word.word}: {word.accuracy_score:.1f}")
