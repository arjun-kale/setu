# rural-ai-assistant-backend

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
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
```

## Run

```bash
# From backend/ directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  
- Health: http://localhost:8000/health  

## Project layout

```
backend/
├── app/
│   ├── main.py           # FastAPI app, lifespan, CORS
│   ├── config/           # Settings, database
│   ├── routes/           # API routes (health, chat, voice, schemes, webhooks)
│   ├── services/         # DynamoDB, S3, scheme, voice, WhatsApp, AI agent
│   ├── models/           # Pydantic schemas, SQLAlchemy models
│   └── utils/            # Logging, helpers
├── requirements.txt
├── .env.example
└── README.md
```

## Database setup (PostgreSQL)

After `.env` has a valid `POSTGRES_URL`:

```bash
cd backend
python scripts/create_tables.py
```

This creates `schemes` and `eligibility_rules` in your database. Then run the app and check `GET /health/db`.

## Planned integrations

- **DynamoDB** — user sessions, chat history
- **PostgreSQL** — scheme data, eligibility rules (tables created via `scripts/create_tables.py`)
- **S3** — audio uploads and TTS output
- **AI agents** — LangGraph + RAG (Pinecone)
- **Voice** — Google STT, Amazon Polly
- **WhatsApp** — Twilio webhook

See `docs/BACKEND_PLAN.md` for phased tasks and project root `PROJECT_CONTEXT.md` for full context.
