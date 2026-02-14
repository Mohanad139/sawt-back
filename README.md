# Sawt Voice Agent

Bilingual (Arabic / English) AI voice agent built on [LiveKit Agents](https://docs.livekit.io/agents/) for **Sawt** — an AI company based in Saudi Arabia.

## Features

- **Bilingual conversation** — Saudi Arabic dialect and English with automatic language detection
- **Real-time voice pipeline** — Deepgram STT, OpenAI LLM, OpenAI TTS, Silero VAD
- **Knowledge base** — comprehensive Sawt company information baked into the system prompt
- **Configurable** — models, voices, and temperature tuneable via environment variables
- **Production-ready** — Dockerfile, structured logging, health-check support

## Architecture

```
User Voice ──▶ Deepgram STT (Nova-3, multilingual)
                       │
                       ▼
              OpenAI GPT-4o-mini  (+ Sawt knowledge base)
                       │
                       ▼
              OpenAI TTS (tts-1)
                       │
                       ▼
              User Voice Output
```

## Project Structure

```
src/sawt/
├── agent.py            # Voice agent & entrypoint
├── config.py           # Settings loaded from env vars
└── prompts/
    └── system.py       # System prompt & greeting
tests/
Dockerfile
pyproject.toml
```

## Prerequisites

| Service | Purpose | Signup |
|---------|---------|--------|
| **LiveKit Cloud** | WebRTC infrastructure | <https://cloud.livekit.io> |
| **Deepgram** | Speech-to-Text | <https://deepgram.com> |
| **OpenAI** | LLM + Text-to-Speech | <https://platform.openai.com> |

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url> && cd sawt-voice-agent

# 2. Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 3. Install the package
pip install -e ".[dev]"

# 4. Configure environment
cp .env.example .env   # then fill in your API keys

# 5. Run locally (development mode)
python -m sawt.agent dev
```

The agent connects to your LiveKit project and waits for voice sessions.

## Configuration

All settings are loaded from environment variables (see `.env.example`).

### Required

| Variable | Description |
|----------|-------------|
| `LIVEKIT_URL` | LiveKit Cloud WebSocket URL |
| `LIVEKIT_API_KEY` | LiveKit API key |
| `LIVEKIT_API_SECRET` | LiveKit API secret |
| `DEEPGRAM_API_KEY` | Deepgram API key |
| `OPENAI_API_KEY` | OpenAI API key |

### Optional (defaults shown)

| Variable | Default | Description |
|----------|---------|-------------|
| `STT_MODEL` | `nova-3` | Deepgram STT model |
| `STT_LANGUAGE` | `multi` | STT language code |
| `LLM_MODEL` | `gpt-4o-mini` | OpenAI chat model |
| `LLM_TEMPERATURE` | `0.7` | LLM sampling temperature |
| `TTS_MODEL` | `tts-1` | OpenAI TTS model |
| `TTS_VOICE` | `alloy` | OpenAI TTS voice |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

## Deployment

### Docker

```bash
docker build -t sawt-agent .
docker run --env-file .env sawt-agent
```

### Railway

The included `railway.toml` handles deployment automatically:

1. Push to a connected GitHub repository
2. Set the required environment variables in the Railway dashboard
3. Railway builds and starts the agent

## Testing the Agent

1. Go to <https://agents-playground.livekit.io>
2. Enter your LiveKit URL and generate a test token
3. Join the room and start talking

## License

Proprietary — all rights reserved.
