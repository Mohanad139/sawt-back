"""Application configuration loaded from environment variables."""

from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def _require_env(name: str) -> str:
    """Return an environment variable or exit with a clear error."""
    value = os.getenv(name, "").strip()
    if not value or value.startswith("your_"):
        logger.critical("Missing required environment variable: %s", name)
        sys.exit(1)
    return value


@dataclass(frozen=True)
class LiveKitSettings:
    url: str = field(default_factory=lambda: _require_env("LIVEKIT_URL"))
    api_key: str = field(default_factory=lambda: _require_env("LIVEKIT_API_KEY"))
    api_secret: str = field(default_factory=lambda: _require_env("LIVEKIT_API_SECRET"))


@dataclass(frozen=True)
class STTSettings:
    """Speech-to-text configuration. Supports 'openai' or 'deepgram' provider."""

    provider: str = field(
        default_factory=lambda: os.getenv("STT_PROVIDER", "openai")
    )
    # OpenAI Whisper settings (default — best Arabic support)
    openai_model: str = field(
        default_factory=lambda: os.getenv("STT_MODEL", "whisper-1")
    )
    openai_language: str = field(
        default_factory=lambda: os.getenv("STT_LANGUAGE", "")
    )
    # Deepgram settings (fallback)
    deepgram_model: str = field(
        default_factory=lambda: os.getenv("STT_DEEPGRAM_MODEL", "nova-3")
    )
    deepgram_language: str = field(
        default_factory=lambda: os.getenv("STT_DEEPGRAM_LANGUAGE", "multi")
    )


@dataclass(frozen=True)
class LLMSettings:
    """OpenAI LLM configuration."""

    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o"))
    temperature: float = field(
        default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0.3"))
    )


@dataclass(frozen=True)
class TTSSettings:
    """Text-to-speech configuration. Supports 'elevenlabs' or 'openai' provider."""

    provider: str = field(
        default_factory=lambda: os.getenv("TTS_PROVIDER", "elevenlabs")
    )
    # ElevenLabs settings
    elevenlabs_model: str = field(
        default_factory=lambda: os.getenv("TTS_MODEL", "eleven_flash_v2_5")
    )
    elevenlabs_voice_id: str = field(
        default_factory=lambda: os.getenv("TTS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
    )
    elevenlabs_language: str = field(
        default_factory=lambda: os.getenv("TTS_LANGUAGE", "ar")
    )
    # OpenAI settings (fallback)
    openai_model: str = field(
        default_factory=lambda: os.getenv("TTS_OPENAI_MODEL", "tts-1")
    )
    openai_voice: str = field(
        default_factory=lambda: os.getenv("TTS_OPENAI_VOICE", "alloy")
    )


@dataclass(frozen=True)
class Settings:
    """Root application settings."""

    livekit: LiveKitSettings = field(default_factory=LiveKitSettings)
    stt: STTSettings = field(default_factory=STTSettings)
    llm: LLMSettings = field(default_factory=LLMSettings)
    tts: TTSSettings = field(default_factory=TTSSettings)
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper()
    )


def get_settings() -> Settings:
    """Create and validate application settings."""
    _require_env("OPENAI_API_KEY")
    settings = Settings()
    if settings.stt.provider == "deepgram":
        _require_env("DEEPGRAM_API_KEY")
    if settings.tts.provider == "elevenlabs":
        _require_env("ELEVEN_API_KEY")
    return settings
