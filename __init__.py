# pronunciation_assessor/__init__.py
__version__ = "1.0.0"
__author__ = "Your Name <your.email@example.com>"
__license__ = "MIT"

from .core.assessment_engine import PronunciationAssessmentEngine
from .core.language_manager import LanguageManager

__all__ = ['PronunciationAssessmentEngine', 'LanguageManager']