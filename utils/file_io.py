import json
from pathlib import Path
from typing import Union, Dict, Any
from datetime import datetime

from ..config.settings import settings
from ..utils.logger import logger


class FileIO:
    @staticmethod
    def save_audio(data: bytes, filename: str) -> Path:
        """Save audio data to file"""
        try:
            output_path = settings.audio_samples_dir / filename
            with open(output_path, 'wb') as f:
                f.write(data)
            logger.info(f"Audio saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to save audio: {str(e)}")
            raise

    @staticmethod
    def save_results(results: Dict[str, Any], filename: str) -> Path:
        """Save assessment results to JSON file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}.json" if not filename.endswith(".json") else filename
            output_path = settings.results_dir / filename

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            logger.info(f"Results saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to save results: {str(e)}")
            raise

    @staticmethod
    def load_results(filepath: Union[str, Path]) -> Dict[str, Any]:
        """Load assessment results from JSON file"""
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                raise FileNotFoundError(f"File not found: {filepath}")

            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load results: {str(e)}")
            raise