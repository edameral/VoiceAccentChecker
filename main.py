import argparse
from pathlib import Path
from typing import Optional

from VoiceAccentChecker.core.assessment_engine import PronunciationAssessmentEngine, AssessmentConfig
from VoiceAccentChecker.core.language_manager import LanguageManager
from VoiceAccentChecker.models.assessment_result import PronunciationAssessmentResult
from VoiceAccentChecker.utils.file_io import FileIO
from VoiceAccentChecker.utils.display import show_results
from VoiceAccentChecker.utils.logger import logger
from VoiceAccentChecker.config.settings import settings


def main():
    parser = argparse.ArgumentParser(
        description="Azure Pronunciation Assessment Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Input arguments
    parser.add_argument("audio_path", help="Path to audio file or directory")
    parser.add_argument("reference_text", help="Reference text for pronunciation assessment")

    # Optional arguments
    parser.add_argument("-l", "--language", default=settings.default_language,
                        help="Language code for assessment (e.g., en-US, tr-TR)")
    parser.add_argument("-o", "--output", help="Output file path for results")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    try:
        # Initialize components
        language_manager = LanguageManager()
        assessment_engine = PronunciationAssessmentEngine()

        # Validate language
        if not language_manager.validate_language(args.language):
            raise ValueError(f"Unsupported language: {args.language}")

        # Process audio input
        audio_path = Path(args.audio_path)

        # Create assessment config
        config = AssessmentConfig(
            reference_text=args.reference_text,
            language=args.language
        )

        # Perform assessment
        if audio_path.is_file():
            result = assessment_engine.assess_pronunciation(str(audio_path), config)
            show_results(result)

            # Save results
            if args.output:
                FileIO.save_results(result.dict(), args.output)
        elif audio_path.is_dir():
            # Batch processing for directory
            for audio_file in audio_path.glob("*.wav"):
                try:
                    print(f"\nProcessing: {audio_file.name}")
                    result = assessment_engine.assess_pronunciation(str(audio_file), config)
                    show_results(result)

                    # Save results with same name as audio file
                    if args.output:
                        output_file = f"{audio_file.stem}_result.json"
                        FileIO.save_results(result.dict(), output_file)
                except Exception as e:
                    logger.error(f"Failed to process {audio_file.name}: {str(e)}")
                    continue
        else:
            raise ValueError("Invalid audio path. Must be a file or directory.")

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise


if __name__ == "__main__":
    main()