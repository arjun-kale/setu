# Setu Backend — What We Built, How It Works, What's Left

---

## 1. What We Built Till Now

| Feature | Endpoint | Status | Description |
|---------|----------|--------|--------------|
| **Health** | `GET /`, `GET /health`, `GET /health/db`, `GET /health/dynamo` | ✅ Done | Service, DB, DynamoDB health checks |
| **Chat** | `POST /api/chat` | ✅ Done | Text chat with session, AI response, DynamoDB storage |
| **Scheme discovery** | `GET /api/schemes`, `GET /api/schemes/{id}` | ✅ Done | List and detail of government schemes from PostgreSQL |
| **Eligibility check** | `POST /api/check-eligibility` | ✅ Done | Match user profile (age, income, state, occupation) to eligible schemes |
| **Voice** | `POST /api/voice` | ✅ Done | Audio in → Whisper STT → Chat → Polly TTS → Audio out |

### Tech Stack (Built)

- **FastAPI** — All APIs
- **PostgreSQL** — Schemes, eligibility rules
- **DynamoDB** — Users, sessions, chat history
- **Whisper (faster-whisper)** — Speech-to-text (free, local)
- **Amazon Polly** — Text-to-speech
- **AWS S3** — Configured (not yet used for audio storage)

---

## 2. How Each Feature Works

### Chat (`POST /api/chat`)

```
1. Frontend sends: { user_id, message, language }
2. Backend creates/gets user + session in DynamoDB
3. Saves user message in messages table
4. Calls AI agent (mock for now) with chat history
5. Saves AI response in DynamoDB
6. Returns { response, session_id }
```

### Scheme Discovery (`GET /api/schemes`, `GET /api/schemes/{id}`)

```
1. Frontend calls GET /api/schemes → list of schemes
2. Frontend calls GET /api/schemes/1 → single scheme detail
3. Backend reads from PostgreSQL (schemes, scheme_eligibility, scheme_documents)
```

### Eligibility Check (`POST /api/check-eligibility`)

```
1. Frontend sends: { age, income, state, occupation }
2. Backend queries PostgreSQL scheme_eligibility
3. Matches user profile to rules
4. Returns list of eligible schemes
```

### Voice (`POST /api/voice`)

```
1. Frontend uploads audio file (WAV, WebM, OGG, FLAC, MP3)
2. Backend: Whisper converts speech → text
3. Backend: Sends text to chat pipeline (same as POST /api/chat)
4. Backend: Polly converts AI response → speech (MP3)
5. Backend returns MP3 audio file
```

---

## 3. Workflow (End-to-End)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Your friend's repo)                     │
│  • Web UI (chat, voice recorder, scheme search, eligibility form)         │
│  • Calls backend APIs                                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         BACKEND (This repo - setu-backend)              │
│                                                                         │
│  POST /api/chat          → DynamoDB (session) → AI agent → DynamoDB     │
│  POST /api/voice         → Whisper STT → Chat flow → Polly TTS → MP3   │
│  GET  /api/schemes       → PostgreSQL schemes                            │
│  GET  /api/schemes/{id}  → PostgreSQL scheme detail                      │
│  POST /api/check-eligibility → PostgreSQL scheme_eligibility            │
│                                                                         │
│  Data: DynamoDB (users, sessions, messages) + PostgreSQL (schemes)      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Frontend Role (What Your Friend Builds)

| Frontend Task | Backend API Used |
|---------------|------------------|
| **Chat UI** | `POST /api/chat` with `user_id`, `message`, `language` |
| **Voice button / recorder** | `POST /api/voice` with `audio` file, `user_id`, `language` |
| **Scheme search / browse** | `GET /api/schemes`, `GET /api/schemes/{id}` |
| **Eligibility form** | `POST /api/check-eligibility` with `age`, `income`, `state`, `occupation` |
| **Session / user ID** | Frontend generates or gets from auth; passes as `user_id` |

**Frontend does NOT:**
- Store chat history (backend does in DynamoDB)
- Run AI logic (backend does)
- Do STT/TTS (backend does)
- Query schemes directly (backend does)

**Frontend DOES:**
- Send HTTP requests to backend
- Display responses (text, JSON, audio)
- Handle UI (forms, buttons, voice recorder)
- Manage auth (if any) and pass `user_id`

---

## 5. What's Remaining to Build

See **`docs/BUILD_PLAN.md`** for full plan.

| # | Feature | Owner |
|---|---------|-------|
| 1 | Intent detection | Us |
| 2 | S3 audio storage | Us |
| 3 | Auth | Us |
| 4 | Skill learning flow | Us |
| 5 | Twilio WhatsApp webhook | Us (last) |
| — | LangGraph + RAG | Friend |

**Order:** Intent → S3 → Auth → Skill learning → Twilio (last). LangGraph/RAG excluded (friend).

---

## 6. Run Commands

```bash
# Install deps
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test all features
python scripts/test_backend_features.py
```

---

## 7. .env Summary

| Variable | Purpose |
|----------|---------|
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` | DynamoDB, Polly, S3 |
| `POSTGRES_URL` | PostgreSQL schemes |
| `STT_PROVIDER=whisper` | Free speech-to-text (no Google) |
| `WHISPER_MODEL_SIZE=base` | Whisper model size |
| `POLLY_VOICE_ID=Joanna` | Polly voice for TTS |
