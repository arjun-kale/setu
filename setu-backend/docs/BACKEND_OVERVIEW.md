# Setu Backend — Full Overview & Code Review

## 1. Architecture Overview

### Tech Stack

| Layer | Technology |
|-------|------------|
| **Framework** | FastAPI |
| **Database (relational)** | PostgreSQL + SQLAlchemy |
| **Database (NoSQL)** | DynamoDB (users, sessions, messages, user_profiles) |
| **Object storage** | AWS S3 (audio files) |
| **Voice STT** | faster-whisper (default) or Google Speech-to-Text |
| **Voice TTS** | Amazon Polly |
| **Messaging** | Twilio WhatsApp API |
| **Auth** | JWT (python-jose) + bcrypt |
| **Config** | pydantic-settings, python-dotenv |

### Folder Structure

```
Setu-Backend/
├── app/
│   ├── __init__.py          # __version__
│   ├── main.py              # FastAPI app entrypoint
│   ├── config/
│   │   ├── settings.py      # Pydantic Settings from env
│   │   └── database.py      # SQLAlchemy engine, session
│   ├── models/
│   │   ├── scheme.py        # Scheme, SchemeEligibility, SchemeDocument
│   │   └── schemas.py       # Pydantic request/response schemas
│   ├── routes/
│   │   ├── auth.py          # Register, Login
│   │   ├── chat.py          # Chat API
│   │   ├── eligibility.py   # Eligibility check
│   │   ├── health.py        # Health checks
│   │   ├── schemes.py       # Scheme discovery
│   │   ├── skills.py        # Digital skills content
│   │   ├── users.py         # User profile
│   │   ├── voice.py         # Voice assistant
│   │   └── webhooks.py      # Twilio WhatsApp webhook
│   ├── services/
│   │   ├── ai_agent.py           # Mock AI (future: LangGraph + RAG)
│   │   ├── auth_service.py       # Password hash, JWT
│   │   ├── dynamodb_service.py   # Users, sessions, messages
│   │   ├── eligibility_service.py
│   │   ├── intent_detection.py   # Rule-based intent
│   │   ├── message_handler.py    # Central routing
│   │   ├── scheme_service.py
│   │   ├── skill_service.py
│   │   ├── voice_service.py      # STT + TTS
│   │   └── whatsapp_service.py   # Twilio send
│   └── utils/
│       └── logging.py
├── docs/
├── scripts/
│   └── test_backend_features.py
├── .env.example
└── requirements.txt
```

---

## 2. Routes — Complete Reference

| Method | Path | Purpose |
|--------|------|---------|
| **GET** | `/` | Root info (service, version, docs link) |
| **GET** | `/health` | Liveness check |
| **GET** | `/health/db` | PostgreSQL connectivity |
| **GET** | `/health/dynamo` | DynamoDB connectivity |
| **POST** | `/webhooks/whatsapp` | Twilio WhatsApp incoming messages |
| **POST** | `/api/auth/register` | User registration |
| **POST** | `/api/auth/login` | User login |
| **POST** | `/api/chat` | Chat message (web/mobile) |
| **GET** | `/api/chat/history` | Chat session history (query: `session_id`, `limit`) |
| **PUT** | `/api/users/{user_id}/profile` | Update user profile |
| **POST** | `/api/voice` | Voice: audio in → transcript → chat → TTS → MP3 out |
| **GET** | `/api/schemes` | List schemes (optional `?q=farmer`) |
| **GET** | `/api/schemes/{id}` | Scheme detail |
| **POST** | `/api/check-eligibility` | Check eligibility by age/income/state/occupation |
| **GET** | `/api/skills` | List digital skills |
| **GET** | `/api/skills/{id}` | Skill detail |

### Route Details

#### Health
- **`/health`** — Returns `{status: "healthy", service, version, timestamp}`
- **`/health/db`** — Runs `SELECT 1` on PostgreSQL
- **`/health/dynamo`** — Checks DynamoDB table status

#### Webhooks
- **`POST /webhooks/whatsapp`** — Twilio sends `From` and `Body` (form-urlencoded). Backend processes message, sends reply via Twilio, returns `{status: "ok"}`.

#### Auth
- **`POST /api/auth/register`** — `{email, password, name}` → creates user in DynamoDB, returns JWT
- **`POST /api/auth/login`** — `{email, password}` → verifies, returns JWT

#### Chat
- **`POST /api/chat`** — `{user_id, message, language}` → intent detection → scheme/eligibility/skill/chat → returns `{response, session_id}`
- **`GET /api/chat/history`** — Query: `session_id` (required), `limit` (optional, default 50, max 100) → returns `{session_id, messages: [{message_id, role, content, created_at}, ...]}`

#### Voice
- **`POST /api/voice`** — Form: `audio` (file), `user_id`, `language` → STT → chat flow → TTS → S3 upload → returns MP3 with headers

#### Schemes
- **`GET /api/schemes`** — Optional `?q=farmer` for search
- **`GET /api/schemes/{id}`** — Single scheme with eligibility rules

#### Eligibility
- **`POST /api/check-eligibility`** — `{age, income, state, occupation}` → matched schemes

#### Skills
- **`GET /api/skills`** — List of digital literacy topics
- **`GET /api/skills/{id}`** — Single skill content

---

## 3. File-by-File Implementation

### `app/main.py`
- FastAPI app, CORS, lifespan, mounts `api_router`
- Exposes `/docs` (Swagger) and `/redoc`

### `app/config/settings.py`
- Loads `.env` via pydantic-settings
- Fields: AWS, PostgreSQL, S3, DynamoDB, Twilio, STT/TTS, JWT
- `get_settings()` cached with `@lru_cache`

### `app/config/database.py`
- SQLAlchemy engine + session factory
- `get_db_session()` — FastAPI dependency for PostgreSQL

### `app/models/scheme.py`
- **Scheme** — id, name, description, benefits
- **SchemeEligibility** — age_limit, income_limit, state, occupation
- **SchemeDocument** — document_name, document_url

### `app/models/schemas.py`
- Pydantic: `ChatRequest`, `ChatResponse`, `SchemeOut`, `CheckEligibilityRequest/Response`, `RegisterRequest/Response`, `LoginRequest/Response`, `UpdateProfileRequest`

### `app/routes/health.py`
- `/health`, `/health/db`, `/health/dynamo`

### `app/routes/webhooks.py`
- Receives Twilio `From`, `Body`
- Ensures user/session in DynamoDB
- Saves user message → `process_message()` → saves assistant message → `send_whatsapp_message()` → `{status: "ok"}`

### `app/routes/chat.py`
- Same flow as webhook but returns JSON `{response, session_id}`

### `app/routes/voice.py`
- Receives audio file
- `speech_to_text()` → chat flow → `text_to_speech()` → S3 upload → MP3 response

### `app/routes/schemes.py`
- `list_schemes()` — GET with optional `q`
- `get_scheme(id)` — GET by ID

### `app/routes/eligibility.py`
- `check_eligibility()` — POST with age, income, state, occupation

### `app/routes/auth.py`
- `register()` — hash password, create user, JWT
- `login()` — verify password, JWT

### `app/routes/users.py`
- `update_profile()` — PUT user profile in DynamoDB

### `app/routes/skills.py`
- `list_skills()`, `get_skill(id)` — static SKILLS data

### `app/services/message_handler.py`
- **Central router** — `process_message(message, user_id, session_id, ...)`
- Calls `detect_intent()` → branches:
  - `scheme_search` → `search_schemes(db, query)`
  - `eligibility_check` → `get_user_profile()` → `check_eligibility()`
  - `skill_learning` → `get_skill()` / `format_skills_for_chat()`
  - `chat` → `get_ai_response()` (mock)

### `app/services/intent_detection.py`
- Rule-based: keywords for scheme_search, eligibility_check, skill_learning
- Default: `chat`

### `app/services/ai_agent.py`
- Mock responses; placeholder for LangGraph + Pinecone RAG

### `app/services/scheme_service.py`
- `search_schemes(db, query, limit)` — PostgreSQL ILIKE search
- `get_all_schemes(db)`

### `app/services/eligibility_service.py`
- `check_eligibility(db, age, income, state, occupation)` — matches scheme_eligibility rules

### `app/services/skill_service.py`
- Static `SKILLS` list (4 topics: basic smartphone, banking, digilocker, fraud safety)
- `list_skills()`, `get_skill(id)`, `format_skills_for_chat()`

### `app/services/auth_service.py`
- `hash_password()`, `verify_password()` — bcrypt
- `create_access_token()`, `decode_token()` — JWT

### `app/services/voice_service.py`
- `speech_to_text()` — Whisper or Google
- `text_to_speech()` — Amazon Polly

### `app/services/whatsapp_service.py`
- `send_whatsapp_message(to, body)` — Twilio REST API

### `app/services/dynamodb_service.py`
- Users, sessions, messages, user_profiles
- `create_user`, `get_user`, `create_session`, `save_message`, `get_chat_history`, `get_user_profile`, `update_user_profile`

---

## 4. How Routes Work — Data Flow

### WhatsApp Message Flow

```
User sends "What schemes for farmers?" on WhatsApp
        │
        ▼
Twilio POST /webhooks/whatsapp
  Body: From=whatsapp:+919923410767, Body=What schemes for farmers?
        │
        ▼
webhooks.whatsapp_webhook()
  ├─ user_id = "whatsapp:+919923410767"
  ├─ dynamo.create_user() if new
  ├─ dynamo.create_session()
  ├─ dynamo.save_message("user", "What schemes for farmers?")
        │
        ▼
message_handler.process_message()
  ├─ intent_detection.detect_intent() → "scheme_search"
  ├─ scheme_service.search_schemes(db, "What schemes for farmers?")
  ├─ PostgreSQL: SELECT * FROM schemes WHERE name/description/benefits ILIKE '%farmer%'
  ├─ Returns formatted scheme list
        │
        ▼
dynamo.save_message("assistant", response)
whatsapp_service.send_whatsapp_message(to=user_id, body=response)
        │
        ▼
Twilio delivers reply to user's WhatsApp
Return {"status": "ok"}
```

### Chat API Flow (Same Logic)

```
POST /api/chat {user_id: "web-user-1", message: "Hello", language: "en"}
        │
        ▼
chat.chat() → process_message() → intent "chat" → get_ai_response() (mock)
        │
        ▼
Return {response: "...", session_id: "web-user-1"}
```

### Voice Flow

```
POST /api/voice (audio file, user_id, language)
        │
        ▼
voice_service.speech_to_text(audio) → "What schemes for farmers?"
        │
        ▼
Same process_message() flow as chat
        │
        ▼
voice_service.text_to_speech(response) → MP3 bytes
s3_client.upload_audio() → S3 URL
        │
        ▼
Return MP3 + headers (X-Transcript, X-Response-Text, X-S3-Input-Url, X-S3-Output-Url)
```

### Scheme Search (Direct API)

```
GET /api/schemes?q=farmer
        │
        ▼
scheme_service.search_schemes(db, query="farmer")
        │
        ▼
PostgreSQL: schemes + eligibility (joinedload)
        │
        ▼
Return {schemes: [{id, name, description, benefits, eligibility_rules}, ...]}
```

### Eligibility Check

```
POST /api/check-eligibility {age: 25, income: 100000, state: "MH", occupation: "farmer"}
        │
        ▼
eligibility_service.check_eligibility(db, ...)
  For each scheme_eligibility row: _eligibility_row_matches()
  Match age range, income max, state, occupation
        │
        ▼
Return {schemes: [matched schemes]}
```

---

## 5. Code Review

### Strengths
- Clear separation: routes → services → data
- Single `process_message()` for chat, WhatsApp, voice
- Pydantic validation on all APIs
- Dependency injection (DB, DynamoDB)
- Health checks for monitoring
- Config via env, no hardcoded secrets

### Patterns
- FastAPI `Depends()` for DB/session
- Service layer abstraction
- Rule-based intent (keyword matching)

### Improvements to Consider
| Area | Suggestion |
|------|------------|
| AI | Replace mock with LangGraph + RAG |
| Auth | Add `get_current_user` dependency for protected routes |
| Intent | ML-based or hybrid intent detection |
| Skills | Move from hardcoded list to DB/config |
| CORS | Restrict `allow_origins` in production |
| JWT | Require strong `JWT_SECRET` in production |

---

## 6. Quick Reference — Intent Keywords

| Intent | Keywords (examples) |
|--------|---------------------|
| scheme_search | scheme, schemes, yojana, farmer, kisan, search, find |
| eligibility_check | eligible, eligibility, age, income, occupation |
| skill_learning | learn, skill, digital, training, course |
| chat | (default) everything else |

---

## 7. Environment Variables (.env)

| Variable | Purpose |
|----------|---------|
| AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION | AWS (DynamoDB, S3, Polly) |
| POSTGRES_URL | PostgreSQL connection string |
| S3_BUCKET_NAME | Audio storage bucket |
| DYNAMODB_* | DynamoDB tables (users, messages, etc.) |
| TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER | WhatsApp |
| STT_PROVIDER | whisper or google |
| JWT_SECRET | JWT signing key |
