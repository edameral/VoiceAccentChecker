import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator

BASE_DIR = Path(__file__).resolve().parent.parent


dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Debug çıktısı (opsiyonel)
print(" BASE_DIR:", BASE_DIR)
print(" .env bulundu mu?", dotenv_path.exists())
print(" Yüklenen Azure Key:", os.getenv("AZURE_SPEECH_KEY"))

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

    # ✅ Pydantic v2 uyumlu yapılandırma
    model_config = SettingsConfigDict(
        env_file=str(dotenv_path),
        env_file_encoding="utf-8"
    )

    @validator("audio_samples_dir", "results_dir", "log_file", pre=True)
    def ensure_dirs_exist(cls, v):
        path = Path(v)  # 🛠️ düz string bile gelse Path'e çevir
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

settings = Settings()
