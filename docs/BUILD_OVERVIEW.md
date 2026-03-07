# Rural AI Assistant Backend — Build Overview

Full overview of **what was built**, **how it was built**, and the **workflow** of built features up to this stage.

---

## 1. What We Built (Summary)

| Area | Status | What exists |
|------|--------|-------------|
| **Project context** | Done | `PROJECT_CONTEXT.md` — purpose, features, architecture |
| **FastAPI app** | Done | `backend/app/main.py` — app, CORS, lifespan, route mount |
| **Environment config** | Done | `.env` + `app/config/settings.py` — all required/optional vars |
| **PostgreSQL** | Done | Models + DB connection; tables: `schemes`, `scheme_eligibility`, `scheme_documents` |
| **DynamoDB** | Done | Two layers: legacy client (sessions/chat) + **DynamoDBService** (users, sessions, messages, user_profiles) |
| **Health APIs** | Done | `GET /health`, `GET /health/db`, `GET /health/dynamo` |
| **Scripts** | Done | Create Postgres tables; create DynamoDB tables (legacy + service) |
| **Git** | Done | Backend on branch `backend` (arjun-kale/setu); copy on cybercomet-07/setu-backend |

**Not built yet (planned):** Scheme discovery API, eligibility API, chat API, S3 usage, Twilio webhook, voice pipeline, AI/RAG.

---

## 2. How We Built It — Tech Stack & Structure

### 2.1 Tech stack

- **Framework:** FastAPI  
- **Config:** python-dotenv, pydantic-settings  
- **PostgreSQL:** SQLAlchemy, psycopg2; connection URL in env  
- **DynamoDB:** boto3 (region ap-south-1 for service tables)  
- **AWS:** S3 bucket name and credentials in env (for future use)

### 2.2 Repository layout

```
Setu-Backend/
├── PROJECT_CONTEXT.md          # Product & architecture (single source of truth)
├── docs/
│   ├── BUILD_OVERVIEW.md       # This file
│   ├── GIT_WORKFLOW.md        # Branch strategy (main vs backend)
│   └── GETTING_CREDENTIALS.md # How to get AWS, Postgres, Twilio, Google keys
│
└── backend/
    ├── .env                    # Secrets (not committed)
    ├── .env.example            # Template for required vars
    ├── requirements.txt
    ├── README.md
    │
    ├── app/
    │   ├── main.py             # FastAPI app, CORS, lifespan, router
    │   ├── config/
    │   │   ├── settings.py     # Env-based settings (AWS, Postgres, S3, DynamoDB, Twilio, Google)
    │   │   └── database.py     # SQLAlchemy engine, SessionLocal, Base, get_db_session
    │   ├── routes/
    │   │   ├── __init__.py     # api_router mounts
    │   │   └── health.py       # /health, /health/db, /health/dynamo
    │   ├── models/
    │   │   ├── scheme.py       # Scheme, SchemeEligibility, SchemeDocument (Postgres)
    │   │   ├── schemas.py      # Pydantic schemas (e.g. HealthResponse)
    │   │   └── db.py           # Re-exports for models
    │   ├── services/
    │   │   ├── dynamodb_client.py   # Legacy: sessions + chat (rural_ai_sessions, rural_ai_chat_history)
    │   │   ├── dynamodb_service.py  # Reusable class: users, sessions, messages, user_profiles (ap-south-1)
    │   │   ├── scheme_service.py    # Placeholder (Postgres scheme/eligibility logic)
    │   │   ├── s3_client.py         # Placeholder
    │   │   ├── voice_service.py     # Placeholder (STT/TTS)
    │   │   ├── whatsapp_service.py   # Placeholder (Twilio)
    │   │   └── ai_agent.py          # Placeholder (LangGraph + RAG)
    │   └── utils/
    │       └── logging.py
    │
    └── scripts/
        ├── create_tables.py              # Postgres: schemes, scheme_eligibility, scheme_documents
        ├── create_dynamodb_tables.py     # DynamoDB legacy: rural_ai_sessions, rural_ai_chat_history
        └── create_dynamodb_service_tables.py  # DynamoDB service: users, sessions, messages, user_profiles
```

---

## 3. What Was Built — Component by Component

### 3.1 Environment and config

- **Purpose:** One place for all env-based configuration; app runs without Twilio/Google keys.
- **How:**  
  - `python-dotenv` loads `backend/.env`.  
  - `pydantic-settings` in `app/config/settings.py` defines required (AWS, Postgres, S3) and optional (Twilio, Google STT) vars.  
  - `get_settings()` returns a cached `Settings` instance.
- **Required in .env:** `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `POSTGRES_URL`, `S3_BUCKET_NAME`.  
- **Optional:** `TWILIO_*`, `GOOGLE_STT_API_KEY`; DynamoDB table names and `DYNAMODB_REGION` (default ap-south-1).

### 3.2 PostgreSQL (schemes data)

- **Purpose:** Store government schemes, eligibility rules, and scheme documents.
- **How:**  
  - SQLAlchemy in `app/config/database.py`: engine from `POSTGRES_URL`, `SessionLocal`, `Base`, `get_db_session()`.  
  - Models in `app/models/scheme.py`:
    - **schemes:** `id`, `name`, `description`, `benefits`
    - **scheme_eligibility:** `id`, `scheme_id`, `age_limit`, `income_limit`, `state`, `occupation`
    - **scheme_documents:** `id`, `scheme_id`, `document_name`, `document_url`
  - Run once: `python scripts/create_tables.py` → creates tables in DB (e.g. SETU-AI).
- **Workflow:** App uses `get_db_session()` in routes; services use the same engine/session for scheme and eligibility queries (to be implemented in `scheme_service`).

### 3.3 DynamoDB — two layers

**A) Legacy client** (`app/services/dynamodb_client.py`)

- **Purpose:** Simple sessions + chat history (original design).
- **Tables:** `rural_ai_sessions` (PK: `session_id`), `rural_ai_chat_history` (PK: `session_id`, SK: `message_id`).
- **Functions:** `get_sessions_table()`, `get_chat_table()`, `create_tables_if_not_exist()`, `get_session()`, `put_session()`, `add_chat_message()`, `get_chat_history()`.
- **Region:** Uses `AWS_REGION` from settings.

**B) DynamoDBService** (`app/services/dynamodb_service.py`)

- **Purpose:** Reusable FastAPI-oriented service for users, sessions, messages, user profiles.
- **Tables (ap-south-1):** `users`, `sessions`, `messages`, `user_profiles`.
- **Functions:**  
  - `create_user(user_id, email=..., name=..., **extra)`  
  - `get_user(user_id)`  
  - `create_session(session_id, user_id=..., **extra)`  
  - `save_message(session_id, role, content, ...)`  
  - `get_chat_history(session_id, limit=50)`  
  - `update_user_profile(user_id, **profile_data)`  
  - `create_tables_if_not_exist()` → creates all four tables if missing.
- **Usage:** Instantiate `DynamoDBService()` or use `get_dynamodb_service()` as a FastAPI dependency.

### 3.4 Health endpoints

- **Purpose:** Liveness/readiness and dependency checks.
- **How:** `app/routes/health.py` mounted on the main app (no prefix).
- **Endpoints:**
  - `GET /health` — app + version + timestamp.
  - `GET /health/db` — runs `SELECT 1` on Postgres via `get_db_session()`.
  - `GET /health/dynamo` — checks DynamoDB by accessing the legacy sessions table (or you can switch to DynamoDBService if desired).

### 3.5 Scripts (run once / when needed)

| Script | Purpose |
|--------|---------|
| `scripts/create_tables.py` | Create Postgres tables: schemes, scheme_eligibility, scheme_documents |
| `scripts/create_dynamodb_tables.py` | Create legacy DynamoDB tables (rural_ai_sessions, rural_ai_chat_history) |
| `scripts/create_dynamodb_service_tables.py` | Create DynamoDBService tables (users, sessions, messages, user_profiles) in ap-south-1 |

---

## 4. Workflow of Built Features (Data Flow)

### 4.1 Request flow (current)

```
Client
  │
  ▼
FastAPI (main.py)
  │
  ├─► GET /         → root info (service name, docs, health link)
  ├─► GET /health   → { status, service, version, timestamp }
  ├─► GET /health/db    → uses get_db_session() → Postgres "SELECT 1" → { database: "ok" | "error: ..." }
  └─► GET /health/dynamo → uses dynamodb_client.get_sessions_table() → { dynamodb: "ok" | "error: ..." }
```

### 4.2 Config and DB workflow

```
.env (backend/.env)
  │
  ▼
load_dotenv() in settings.py
  │
  ▼
Settings (pydantic-settings)
  │
  ├─► database.py  → engine = create_engine(settings.postgres_url) → SessionLocal, get_db_session
  ├─► dynamodb_client.py  → boto3.resource(..., region_name=settings.aws_region)
  └─► dynamodb_service.py → DynamoDBService(region=settings.dynamodb_region, ...)
```

### 4.3 PostgreSQL workflow (for future scheme/eligibility APIs)

```
API route (e.g. /schemes, /eligibility — not built yet)
  │
  ▼
Depends(get_db_session) → Session
  │
  ▼
scheme_service (placeholder) → query Scheme, SchemeEligibility, SchemeDocument
  │
  ▼
PostgreSQL (SETU-AI): schemes, scheme_eligibility, scheme_documents
```

### 4.4 DynamoDB workflow (for future chat/session APIs)

```
API route (e.g. /chat — not built yet)
  │
  ▼
Depends(get_dynamodb_service) → DynamoDBService
  │
  ├─► create_session(session_id, user_id=...)
  ├─► save_message(session_id, role, content)
  ├─► get_chat_history(session_id)
  └─► update_user_profile(user_id, age=..., state=..., ...)
  │
  ▼
DynamoDB (ap-south-1): users, sessions, messages, user_profiles
```

---

## 5. Current State vs Plan

### 5.1 Done

- Project context and backend plan docs  
- FastAPI app with config, health, and CORS  
- Postgres models and tables created (schemes, scheme_eligibility, scheme_documents)  
- DynamoDB: legacy client + DynamoDBService with all required functions and tables created  
- Scripts to create all tables  
- Git: backend on `backend` branch; copy on cybercomet-07/setu-backend  

### 5.2 Next (from BACKEND_PLAN.md)

- **Phase 2:** Scheme discovery API, eligibility API, chat API (using Postgres + DynamoDBService), S3 helpers.  
- **Phase 3:** Twilio webhook, voice (Google STT + Polly), AI/RAG (LangGraph + Pinecone).

---

## 6. Quick reference

| Need | Where |
|------|--------|
| Product/architecture | `PROJECT_CONTEXT.md` |
| Build plan (phases) | `backend/docs/BACKEND_PLAN.md` |
| Git (branch strategy) | `docs/GIT_WORKFLOW.md` |
| Credentials (AWS, Postgres, Twilio, Google) | `backend/docs/GETTING_CREDENTIALS.md` |
| This overview | `docs/BUILD_OVERVIEW.md` |
| Run backend | `cd backend && uvicorn app.main:app --reload` |
| Create Postgres tables | `cd backend && python scripts/create_tables.py` |
| Create DynamoDB service tables | `cd backend && python scripts/create_dynamodb_service_tables.py` |
