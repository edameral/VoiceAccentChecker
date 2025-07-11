class PronunciationAssessmentError(Exception):
    """Base exception for pronunciation assessment"""
    pass

class AssessmentError(PronunciationAssessmentError):
    """Errors during pronunciation assessment"""
    pass

class AudioProcessingError(PronunciationAssessmentError):
    """Errors during audio processing"""
    pass

class LanguageNotSupportedError(PronunciationAssessmentError):
    """Requested language is not supported"""
    pass

class ConfigurationError(PronunciationAssessmentError):
    """Configuration related errors"""
    pass