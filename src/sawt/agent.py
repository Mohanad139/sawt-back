"""Sawt voice agent — LiveKit VoiceAssistant implementation."""

from __future__ import annotations

import logging
from typing import Any

from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.llm import ChatContext, ChatMessage
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, elevenlabs, openai, silero

from sawt.config import Settings, get_settings
from sawt.prompts.system import GREETING, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class SawtVoiceAgent:
    """Bilingual Arabic/English voice agent backed by LiveKit."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._assistant: VoiceAssistant | None = None

    # ------------------------------------------------------------------
    # Pipeline component factories
    # ------------------------------------------------------------------

    def _build_stt(self) -> deepgram.STT:
        cfg = self._settings.stt
        return deepgram.STT(
            model=cfg.model,
            language=cfg.language,
            smart_format=True,
            punctuate=True,
        )

    def _build_llm(self) -> openai.LLM:
        cfg = self._settings.llm
        return openai.LLM(
            model=cfg.model,
            temperature=cfg.temperature,
        )

    def _build_tts(self) -> elevenlabs.TTS | openai.TTS:
        cfg = self._settings.tts
        if cfg.provider == "elevenlabs":
            return elevenlabs.TTS(
                model=cfg.elevenlabs_model,
                voice=elevenlabs.Voice(
                    id=cfg.elevenlabs_voice_id, name="", category="premade"
                ),
                language=cfg.elevenlabs_language,
            )
        return openai.TTS(
            model=cfg.openai_model,
            voice=cfg.openai_voice,
        )

    # ------------------------------------------------------------------
    # Entrypoint
    # ------------------------------------------------------------------

    async def entrypoint(self, ctx: JobContext) -> None:
        """Handle an incoming LiveKit session."""
        logger.info("Starting voice agent for room %s", ctx.room.name)

        await ctx.connect()
        logger.info("Connected to room %s", ctx.room.name)

        initial_ctx = ChatContext(
            messages=[ChatMessage(role="system", content=SYSTEM_PROMPT)]
        )

        stt = self._build_stt()
        llm = self._build_llm()
        tts = self._build_tts()

        logger.info(
            "Pipeline: STT=%s | LLM=%s | TTS=%s",
            self._settings.stt.model,
            self._settings.llm.model,
            self._settings.tts.provider,
        )

        self._assistant = VoiceAssistant(
            vad=silero.VAD.load(),
            stt=stt,
            llm=llm,
            tts=tts,
            chat_ctx=initial_ctx,
        )

        self._assistant.start(ctx.room)
        logger.info("Voice assistant started — sending greeting")

        await self._assistant.say(GREETING, allow_interruptions=True)
        logger.info("Agent is fully operational")


def prewarm(proc: Any) -> None:
    """Pre-warm heavy dependencies before the first job arrives."""
    logger.info("Pre-warming agent process")


def main() -> None:
    """Application entrypoint."""
    settings = get_settings()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    agent = SawtVoiceAgent(settings)

    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=agent.entrypoint,
            prewarm_fnc=prewarm,
        )
    )


if __name__ == "__main__":
    main()
