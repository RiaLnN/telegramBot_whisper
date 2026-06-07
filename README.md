# telegramBot_whisper

Telegram bot that transcribes voice messages and supports two AI actions on bot replies:
- short summary
- short conversational answer

Built with Groq Whisper API + LLaMA API, deployed via Docker.

---

## How it works

1. Send a voice message to the bot.
2. Bot returns transcribed text.
3. Reply to **bot text message** with one of the command groups:

**Summary commands:**
`!суть` · `!summary` · `/summary` · `выжимка` · `summary` · `!gist` · `!сенс` · `!коротко`

**Answer commands:**
`!answer` · `!ответь` · `!reply` · `!відповісти` · `/answer` · `!ответ` · `!відповідь`

Voice transcription and AI response language follow the original input.

---

## Stack

- **[aiogram](https://github.com/aiogram/aiogram)** — Telegram bot framework
- **[Groq](https://groq.com)** — Whisper speech-to-text transcription
- **LLaMA API** — summary/answer generation
- **Docker** — containerized deployment

---

## Running

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
GROQ_AUDIO_URL=https://api.groq.com/openai/v1/audio/transcriptions

LLAMA_API_KEY=your_llama_api_key
LLAMA_URL=https://your-llama-endpoint
```

3. Start bot:
```bash
docker compose up --build -d
```

---

## Getting API keys

| Key | Where to get |
|---|---|
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather) in Telegram |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `LLAMA_API_KEY` | your LLaMA provider |
