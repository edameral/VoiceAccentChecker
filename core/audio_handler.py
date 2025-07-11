import io
import wave
import numpy as np
import soundfile as sf
from typing import Union
from pathlib import Path

from ..config.settings import settings
from ..utils.logger import logger
from .exceptions import AudioProcessingError


class AudioHandler:
    def __init__(self):
        self.sample_rate = settings.audio_sample_rate
        self.max_duration = settings.max_audio_duration
        logger.info("Audio Handler initialized")

    def process_audio(self, audio_input: Union[str, bytes, Path]) -> bytes:
        """Process audio input and return standardized audio data"""
        try:
            if isinstance(audio_input, (str, Path)):
                # Read from file
                return self._process_file(audio_input)
            elif isinstance(audio_input, bytes):
                # Process bytes directly
                return self._process_bytes(audio_input)
            else:
                raise AudioProcessingError("Unsupported audio input type")
        except Exception as e:
            logger.error(f"Audio processing failed: {str(e)}")
            raise AudioProcessingError(f"Audio processing failed: {str(e)}")

    def _process_file(self, file_path: Union[str, Path]) -> bytes:
        """Process audio file"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise AudioProcessingError(f"Audio file not found: {file_path}")

        # Read audio file
        data, sr = sf.read(file_path, dtype='float32')

        # Resample if necessary
        if sr != self.sample_rate:
            data = self._resample_audio(data, sr, self.sample_rate)

        # Convert to WAV format in memory
        return self._convert_to_wav_bytes(data, self.sample_rate)

    def _process_bytes(self, audio_bytes: bytes) -> bytes:
        """Process audio bytes"""
        try:
            # Try to read as WAV
            with wave.open(io.BytesIO(audio_bytes)) as wav_file:
                sr = wav_file.getframerate()
                n_frames = wav_file.getnframes()
                data = np.frombuffer(wav_file.readframes(n_frames), dtype=np.int16)
                data = data.astype(np.float32) / 32768.0  # Convert to float32
        except:
            # If not WAV, try with soundfile
            try:
                with io.BytesIO(audio_bytes) as audio_stream:
                    data, sr = sf.read(audio_stream, dtype='float32')
            except Exception as e:
                raise AudioProcessingError(f"Unsupported audio format: {str(e)}")

        # Resample if necessary
        if sr != self.sample_rate:
            data = self._resample_audio(data, sr, self.sample_rate)

        return self._convert_to_wav_bytes(data, self.sample_rate)

    def _resample_audio(self, data: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
        """Resample audio data using simple linear interpolation"""
        if orig_sr == target_sr:
            return data

        duration = len(data) / orig_sr
        if duration > self.max_duration:
            raise AudioProcessingError(f"Audio duration exceeds maximum limit of {self.max_duration} seconds")

        # Calculate new length
        new_length = int(len(data) * target_sr / orig_sr)

        # Linear interpolation for resampling
        x_old = np.linspace(0, 1, len(data))
        x_new = np.linspace(0, 1, new_length)
        return np.interp(x_new, x_old, data)

    def _convert_to_wav_bytes(self, data: np.ndarray, sample_rate: int) -> bytes:
        """Convert numpy array to WAV bytes"""
        with io.BytesIO() as wav_buffer:
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes((data * 32767).astype(np.int16))
            return wav_buffer.getvalue()