from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class PhonemeResult(BaseModel):
    phoneme: str
    accuracy_score: float
    pronunciation: Optional[str] = None
    nist_error: Optional[str] = None
    mispronunciation: Optional[str] = None


class WordResult(BaseModel):
    word: str
    accuracy_score: float
    error_type: Optional[str] = None
    phonemes: Optional[List[Dict[str, Union[str, float]]]] = None


class PronunciationAssessmentResult(BaseModel):
    accuracy_score: float = Field(..., ge=0, le=100)
    fluency_score: Optional[float] = Field(None, ge=0, le=100)
    completeness_score: Optional[float] = Field(None, ge=0, le=100)
    pron_score: Optional[float] = Field(None, ge=0, le=100)
    language: str
    reference_text: str
    recognized_text: str
    words: List[WordResult]
    phonemes: Optional[List[PhonemeResult]] = None

    def overall_score(self) -> float:
        """Calculate weighted overall score"""
        weights = {
            'accuracy': 0.4,
            'fluency': 0.3,
            'completeness': 0.3
        }

        scores = {
            'accuracy': self.accuracy_score,
            'fluency': self.fluency_score or 0,
            'completeness': self.completeness_score or 0
        }

        return sum(scores[k] * weights[k] for k in weights)

    def get_mispronounced_words(self) -> List[Dict]:
        """Get list of mispronounced words with details"""
        return [
            {
                "word": word.word,
                "score": word.accuracy_score,
                "error_type": word.error_type
            }
            for word in self.words
            if word.error_type and word.error_type != "None"
        ]

    def get_phoneme_accuracy_stats(self) -> Dict[str, float]:
        """Get statistics about phoneme accuracy"""
        if not self.phonemes:
            return {}

        scores = [p.accuracy_score for p in self.phonemes]
        return {
            "min": min(scores),
            "max": max(scores),
            "average": sum(scores) / len(scores),
            "count": len(scores)
        }