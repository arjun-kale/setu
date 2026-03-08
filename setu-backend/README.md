# Setu Backend — Rural AI Assistant

Production-ready FastAPI backend for **Rural AI Assistant** (schemes, eligibility, voice, WhatsApp).

## Stack

| Component   | Technology |
|------------|------------|
| Framework  | FastAPI |
| NoSQL      | Amazon DynamoDB (sessions, chat) |
| SQL        | PostgreSQL (schemes, eligibility) |
| Storage    | Amazon S3 (audio) |
| Voice STT  | Google Speech-to-Text |
| Voice TTS  | Amazon Polly |
| Messaging  | Twilio WhatsApp API |

## Requirements

- Python 3.9+

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  
- Health: http://localhost:8000/health  

## Voice API

`POST /api/voice` — send audio, get AI response as speech:

1. Accept audio upload (WAV, WebM, OGG, FLAC, MP3)
2. Convert speech to text (**Whisper** — free, local, no API key)
3. Process via chat service
4. Convert response to speech (Amazon Polly)
5. Return MP3 audio

```bash
curl -X POST http://localhost:8000/api/voice \
  -F "audio=@recording.wav" \
  -F "user_id=user123" \
  -F "language=en-IN" \
  -o response.mp3
```

**Speech-to-Text:** Uses **Whisper** (free, runs locally) by default. No Google Cloud or billing needed.  
**Text-to-Speech:** AWS Polly (uses your existing AWS credentials).

## Project layout

```
├── app/
│   ├── main.py           # FastAPI app, lifespan, CORS
│   ├── config/           # Settings, database
│   ├── routes/           # API routes (health, chat, schemes, eligibility)
│   ├── services/         # DynamoDB, S3, scheme, voice, WhatsApp, AI agent
│   ├── models/           # Pydantic schemas, SQLAlchemy models
│   └── utils/            # Logging, helpers
├── scripts/              # DB setup, table creation, tests
├── docs/                 # Documentation
├── requirements.txt
├── .env.example
└── README.md
```

## Database setup (PostgreSQL)

After `.env` has a valid `POSTGRES_URL`:

```bash
python scripts/create_tables.py
```

This creates `schemes`, `scheme_eligibility`, and `scheme_documents` in your database. Then run the app and check `GET /health/db`.

## DynamoDB setup

```bash
python scripts/create_dynamodb_service_tables.py
```

## Test

```bash
python scripts/test_backend_features.py
```

## Planned integrations

- **DynamoDB** — user sessions, chat history ✓
- **PostgreSQL** — scheme data, eligibility rules ✓
- **S3** — audio uploads and TTS output
- **AI agents** — LangGraph + RAG (Pinecone)
- **Voice** — Google STT, Amazon Polly
- **WhatsApp** — Twilio webhook

See `docs/BACKEND_PLAN.md` for phased tasks and `PROJECT_CONTEXT.md` for full context.
