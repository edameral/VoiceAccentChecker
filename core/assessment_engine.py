import os
from typing import Optional, Union
from dataclasses import dataclass
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import PronunciationAssessmentGranularity

from ..config.settings import settings
from ..models.assessment_result import PronunciationAssessmentResult
from .exceptions import AudioProcessingError, AssessmentError
from .audio_handler import AudioHandler
from ..utils.logger import logger


@dataclass
class AssessmentConfig:
    reference_text: str
    language: str = settings.default_language
    granularity: PronunciationAssessmentGranularity = PronunciationAssessmentGranularity.Phoneme
    enable_miscue: bool = True
    phoneme_alphabet: str = "IPA"


class PronunciationAssessmentEngine:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=settings.azure_speech_key,
            region=settings.azure_speech_region
        )
        self.audio_handler = AudioHandler()
        logger.info("Pronunciation Assessment Engine initialized")

    def assess_pronunciation(
            self,
            audio_input: Union[str, bytes],
            config: AssessmentConfig
    ) -> PronunciationAssessmentResult:
        """Assess pronunciation from audio input"""
        try:
            # Process audio input
            audio_data = self.audio_handler.process_audio(audio_input)

            # Create audio stream from memory
            audio_stream = speechsdk.AudioInputStream.create_push_stream(
                speechsdk.AudioStreamFormat(samples_per_second=settings.audio_sample_rate)
            )
            audio_stream.write(audio_data)
            audio_stream.close()

            audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)

            # Configure pronunciation assessment
            pronunciation_config = speechsdk.PronunciationAssessmentConfig(
                reference_text=config.reference_text,
                grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
                granularity=config.granularity,
                enable_miscue=config.enable_miscue,
                phoneme_alphabet=config.phoneme_alphabet
            )

            # Create speech recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config,
                language=config.language
            )

            # Apply pronunciation assessment
            pronunciation_config.apply_to(speech_recognizer)

            # Perform recognition
            result = speech_recognizer.recognize_once_async().get()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return self._parse_result(result, config)
            elif result.reason == speechsdk.ResultReason.NoMatch:
                raise AssessmentError("No speech could be recognized.")
            else:
                raise AssessmentError(f"Speech recognition failed: {result.reason}")

        except Exception as e:
            logger.error(f"Assessment failed: {str(e)}")
            raise AssessmentError(f"Assessment failed: {str(e)}")

    def _parse_result(
            self,
            result: speechsdk.SpeechRecognitionResult,
            config: AssessmentConfig
    ) -> PronunciationAssessmentResult:
        """Parse Azure SDK result into our custom model"""
        pronunciation_result = speechsdk.PronunciationAssessmentResult(result)

        # Detailed phoneme-level results
        phoneme_results = []
        if config.granularity == PronunciationAssessmentGranularity.Phoneme:
            for word in pronunciation_result.words:
                for phoneme in word.phonemes:
                    phoneme_results.append({
                        "phoneme": phoneme.phoneme,
                        "accuracy_score": phoneme.accuracy_score,
                        "pronunciation": phoneme.pronunciation_assessment.pronunciation,
                        "nist_error": phoneme.pronunciation_assessment.nist_error,
                        "mispronunciation": phoneme.pronunciation_assessment.mispronunciation
                    })

        # Word-level results
        word_results = []
        for word in pronunciation_result.words:
            word_results.append({
                "word": word.word,
                "accuracy_score": word.accuracy_score,
                "error_type": word.error_type,
                "phonemes": [{
                    "phoneme": p.phoneme,
                    "accuracy_score": p.accuracy_score
                } for p in word.phonemes] if word.phonemes else []
            })

        # Create result object
        return PronunciationAssessmentResult(
            accuracy_score=pronunciation_result.accuracy_score,
            fluency_score=pronunciation_result.fluency_score,
            completeness_score=pronunciation_result.completeness_score,
            pron_score=pronunciation_result.pronunciation_score,
            language=config.language,
            reference_text=config.reference_text,
            recognized_text=result.text,
            words=word_results,
            phonemes=phoneme_results if phoneme_results else None
        )