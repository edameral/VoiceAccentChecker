import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, validator

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # Azure Configuration
    azure_speech_key: str = Field(..., env="AZURE_SPEECH_KEY")
    azure_speech_region: str = Field(..., env="AZURE_SPEECH_REGION")

    # Application Configuration
    default_language: str = Field("en-US", env="DEFAULT_LANGUAGE")
    audio_sample_rate: int = Field(16000, env="AUDIO_SAMPLE_RATE")
    max_audio_duration: int = Field(60, env="MAX_AUDIO_DURATION")

    # Paths
    audio_samples_dir: Path = BASE_DIR / "data" / "audio_samples"
    results_dir: Path = BASE_DIR / "data" / "results"
    log_file: Path = BASE_DIR / "logs" / "pronunciation_assessment.log"

    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

    @validator("audio_samples_dir", "results_dir", "log_file", pre=True)
    def ensure_dirs_exist(cls, v: Path):
        v.parent.mkdir(parents=True, exist_ok=True)
        return v


settings = Settings()