# TelegramBot_Whisper

Telegram bot for:
- voice message transcription (Groq Whisper)
- concise summary generation
- reply generation to transcribed text

---

## How it works

1. Send a voice message to the bot.
2. Bot returns the recognized text.
3. Reply to that bot message with one of the commands below:
   - summary command → short summary
   - answer command → ready-to-send reply text

Works with voice messages in any language.

---

## Commands

### Summary commands
`!суть` · `!summary` · `/summary` · `выжимка` · `summary` · `!gist` · `!сенс` · `!коротко`

### Answer commands
`!answer` · `!ответь` · `!reply` · `!відповісти` · `/answer` · `!ответ` · `!відповідь`

---

## Stack

- **[aiogram](https://github.com/aiogram/aiogram)** — Telegram bot framework
- **[Groq](https://groq.com)** — speech-to-text (Whisper)
- **LLaMA-compatible chat API** — summary/answer generation
- **Celery + Redis** — background task processing
- **Docker Compose** — service orchestration

---

## Run locally (Docker)

**Requirements:** Docker, Docker Compose

1. Clone repository:
```bash
git clone https://github.com/RiaLnN/telegramBot_whisper.git
cd telegramBot_whisper
```

2. Create `.env`:
```env
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
LLAMA_API_KEY=your_llama_api_key
```
**Note:** `GROQ_AUDIO_URL` and `LLAMA_URL` are already defined in bot constants, so they are not required in `.env`.

3. Start services:
```bash
docker compose up --build -d
```

This starts:
- `bot` — Telegram polling service
- `celery` — async worker for transcription and AI responses
- `redis` — broker for Celery tasks

---

## API keys

| Key | Where to get |
|---|---|
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather) |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `LLAMA_API_KEY` | your LLaMA-compatible provider |