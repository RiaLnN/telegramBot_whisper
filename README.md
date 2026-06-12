# TelegramBot_Whisper

Telegram bot that transcribes voice messages in seconds and optionally summarizes them.
Built with Groq Whisper API + LLaMA, deployed on Azure via Docker.

---

## How it works

1. Send any voice message to the bot
2. Bot instantly returns the transcribed text
3. Reply to that message with a summary command — bot returns a short summary

**Summary commands:** `!суть` · `!summary` · `/summary` · `выжимка` · `summary` · `!gist`

Works with voice messages in any language.

---

## Stack

- **[aiogram](https://github.com/aiogram/aiogram)** — Telegram bot framework
- **[Groq](https://groq.com)** — Whisper-based speech-to-text (near-instant transcription)
- **LLaMA API** — summarization via second LLM call
- **Docker** — single-container deployment

---

## Running

**Requirements:** Docker, Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/RiaLnN/voice-to-text-bot.git
cd voice-to-text-bot
```

2. Create a `.env` file:
```env
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
LLAMA_API_KEY=your_llama_api_key
```

3. Start:
```bash
docker compose up --build -d
```

---

## Getting API keys

| Key | Where to get |
|---|---|
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather) in Telegram |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — free tier available |
| `LLAMA_API_KEY` | depends on your LLaMA provider |