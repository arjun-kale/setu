# Phases, Implementation & Domain Relationships

Based on the workflow diagram ΓÇö phases to build, how they're implemented, and how backend relates to frontend, automation, and other domains.

---

## 1. Build Phases (From Workflow Diagram)

### Phase 1: User Input & Ingestion
**Diagram components:** User (Web PWA / WhatsApp) ΓåÆ API Routes / Twilio Webhook

| Component | Purpose |
|-----------|---------|
| Web PWA | User chats via web |
| WhatsApp | User chats via WhatsApp |
| API (chat, voice) | Receive text or voice from web |
| Twilio Webhook | Receive messages from WhatsApp |

---

### Phase 2: Core Processing
**Diagram components:** Lambda chat-process / Lambda voice-ingest ΓåÆ S3, SQS

| Component | Purpose |
|-----------|---------|
| Chat processor | Handle incoming chat, run intent + routing |
| Voice ingest | Receive audio, store in S3, queue for processing |
| S3 (audio) | Store voice input/output |
| SQS (voice queue) | Async voice processing (optional) |

---

### Phase 3: Orchestration & Agents
**Diagram components:** Python Agents (LangGraph) ΓåÆ DocBridge, Siriwani, Scheme Compass, Bhasha, DynamoDB, TTS

| Component | Purpose |
|-----------|---------|
| LangGraph Orchestrator | Route to agents, coordinate flow |
| Scheme Compass | Eligibility + RAG for schemes |
| Siriwani | Skills + Quiz |
| DocBridge | Document AI |
| Bhasha | Language/dialect |
| DynamoDB | Memory, user profile |
| TTS (Polly) | Text to speech |

---

### Phase 4: Output & UI
**Diagram components:** Next.js ΓåÆ User UI (Chat, Schemes, Loan, Documents, Profile)

| Component | Purpose |
|-----------|---------|
| Next.js | Frontend app |
| User UI | Chat, schemes, loan, documents, profile screens |

---

## 2. How Each Phase Is Implemented (Backend)

### Phase 1: User Input & Ingestion Γ£à

| Diagram | Backend Implementation | Why |
|---------|------------------------|-----|
| Web PWA ΓåÆ API | `POST /api/chat`, `POST /api/voice` | Single entry for web chat and voice |
| WhatsApp ΓåÆ Webhook | `POST /webhooks/whatsapp` | Twilio sends here; same logic as web |
| API Routes | FastAPI routes (no Lambda) | Simpler to run and debug; can move to Lambda later |

---

### Phase 2: Core Processing Γ£à

| Diagram | Backend Implementation | Why |
|---------|------------------------|-----|
| Chat processor | `message_handler.process_message()` | Central handler for chat and voice text |
| Voice ingest | Inside `POST /api/voice` | STT ΓåÆ process_message ΓåÆ TTS in one request |
| S3 (audio) | `s3_client.upload_audio()` | Store input/output audio |
| SQS | Not used | Sync flow is enough for now; SQS can be added later |

---

### Phase 3: Orchestration & Agents ΓÜá∩╕Å Partial

| Diagram | Backend Implementation | Why |
|---------|------------------------|-----|
| LangGraph Orchestrator | `intent_detection` + `message_handler` | Rule-based routing; AI team will add LangGraph |
| Scheme Compass | `scheme_service`, `eligibility_service` + PostgreSQL | Structured scheme data; RAG handled by AI team |
| Siriwani | `skill_service` (static content) | Simple skills; quiz to be added |
| DocBridge | Not implemented | Assigned to AI/other team |
| Bhasha | Not implemented | Assigned to AI/other team |
| DynamoDB | `dynamodb_service` | Users, sessions, messages, profiles |
| TTS | `voice_service.text_to_speech()` (Polly) | Voice replies |

---

### Phase 4: Output & UI Γ£à (Backend Side)

| Diagram | Backend Implementation | Why |
|---------|------------------------|-----|
| Response to web | JSON `{response, session_id}` | Frontend consumes this |
| Response to WhatsApp | `whatsapp_service.send_whatsapp_message()` | Twilio sends reply |
| Response to voice | MP3 + S3 URLs in headers | Frontend plays or stores audio |
| Schemes, eligibility, skills | REST APIs | Frontend calls these directly |

---

## 3. Domain Relationships

### 3.1 Backend Γåö Frontend

| Backend Provides | Frontend Uses | Purpose |
|------------------|---------------|---------|
| `POST /api/chat` | Send message, get reply | Chat UI |
| `GET /api/chat/history` | Load past messages | Chat history |
| `POST /api/voice` | Send audio, get MP3 | Voice UI |
| `GET /api/schemes` | List schemes | Schemes screen |
| `GET /api/schemes/{id}` | Scheme detail | Scheme detail screen |
| `POST /api/check-eligibility` | Check eligibility | Eligibility screen |
| `GET /api/skills` | List skills | Skills screen |
| `PUT /api/users/{id}/profile` | Update profile | Profile screen |
| `POST /api/auth/register`, `POST /api/auth/login` | Auth | Login/register |

**Flow:** Frontend ΓåÆ HTTP ΓåÆ Backend ΓåÆ DB/Services ΓåÆ Response ΓåÆ Frontend

---

### 3.2 Backend Γåö Automation (RAG / LangGraph)

| Backend Provides | Automation (AI Team) Uses | Purpose |
|------------------|---------------------------|---------|
| `get_ai_response()` interface | Replace with LangGraph call | Chat intent handling |
| `chat_history` (format) | Context for AI | Conversation memory |
| `user_profile` (age, income, state, occupation) | Context for AI | Personalization |
| `message`, `language`, `session_id`, `user_id` | Input to AI | Request context |
| Scheme data (PostgreSQL) | RAG ingestion (optional) | Scheme search |
| DynamoDB (messages) | Read/write by backend | AI does not touch DB directly |

**Flow:** Backend ΓåÆ calls AI service (when enabled) ΓåÆ AI returns text ΓåÆ Backend stores and returns

**Contract:** Backend defines input/output; AI team implements the service.

---

### 3.3 Backend Γåö WhatsApp (Twilio)

| Backend Provides | Twilio Uses | Purpose |
|------------------|-------------|---------|
| `POST /webhooks/whatsapp` | Webhook URL | Receive messages |
| `send_whatsapp_message()` | Twilio REST API | Send replies |

**Flow:** User ΓåÆ WhatsApp ΓåÆ Twilio ΓåÆ Backend webhook ΓåÆ process_message ΓåÆ Twilio API ΓåÆ User

---

### 3.4 Backend Γåö External Services

| Service | Backend Uses | Purpose |
|---------|--------------|---------|
| **PostgreSQL** | Schemes, eligibility | Structured scheme data |
| **DynamoDB** | Users, sessions, messages, profiles | Session and user state |
| **S3** | Audio storage | Voice input/output |
| **Twilio** | WhatsApp API | Send/receive WhatsApp |
| **Polly** | TTS | Voice replies |
| **Whisper / Google STT** | Speech-to-text | Voice input |

---

## 4. How Components Work in the Full Application

### 4.1 Chat Flow (Web)

```
User (Frontend) ΓåÆ POST /api/chat
    ΓåÆ Backend: create user/session, save message
    ΓåÆ intent_detection ΓåÆ scheme_search | eligibility | skill_learning | chat
    ΓåÆ If chat: get_ai_response() [mock now; AI team will replace]
    ΓåÆ Save response, return JSON
    ΓåÆ Frontend displays reply
```

**Domains:** Frontend (UI) Γåö Backend (logic, storage) Γåö Automation (AI when integrated)

---

### 4.2 Chat Flow (WhatsApp)

```
User (WhatsApp) ΓåÆ Twilio ΓåÆ POST /webhooks/whatsapp
    ΓåÆ Backend: same process_message() as web
    ΓåÆ send_whatsapp_message() ΓåÆ Twilio ΓåÆ User
```

**Domains:** WhatsApp Γåö Twilio Γåö Backend (logic) Γåö Automation (AI when integrated)

---

### 4.3 Voice Flow

```
User (Frontend) ΓåÆ POST /api/voice (audio)
    ΓåÆ Backend: STT ΓåÆ process_message() ΓåÆ TTS ΓåÆ S3
    ΓåÆ Return MP3 + S3 URLs
    ΓåÆ Frontend plays audio
```

**Domains:** Frontend (record/play) Γåö Backend (STT, logic, TTS, S3)

---

### 4.4 Schemes / Eligibility (Direct API)

```
User (Frontend) ΓåÆ GET /api/schemes or POST /api/check-eligibility
    ΓåÆ Backend: PostgreSQL query
    ΓåÆ Return JSON
    ΓåÆ Frontend displays list/detail
```

**Domains:** Frontend Γåö Backend Γåö PostgreSQL

---

### 4.5 Profile

```
User (Frontend) ΓåÆ PUT /api/users/{id}/profile
    ΓåÆ Backend: DynamoDB update
    ΓåÆ Used later by eligibility + AI (user context)
```

**Domains:** Frontend Γåö Backend Γåö DynamoDB Γåö Eligibility Γåö Automation (AI context)

---

## 5. Summary Table: Backend Work by Domain

| Domain | Backend Responsibility | Status |
|--------|------------------------|--------|
| **Frontend** | REST APIs for chat, voice, schemes, eligibility, skills, auth, profile | Γ£à Done |
| **Automation (AI)** | Stable `get_ai_response` interface, config, user_profile, chat_history | ΓÜá∩╕Å Prep done; AI team integrates |
| **WhatsApp** | Webhook, Twilio send | Γ£à Done |
| **Data** | PostgreSQL (schemes), DynamoDB (users, sessions, messages) | Γ£à Done |
| **Voice** | STT, TTS, S3 | Γ£à Done |
| **Auth** | Register, login, JWT | Γ£à Done |

---

## 6. What Backend Must Provide for Other Domains

### For Frontend
- All REST APIs documented (OpenAPI/Swagger at `/docs`)
- CORS enabled
- Consistent JSON schemas
- Error responses (400, 401, 404)

### For Automation (AI Team)
- `get_ai_response(message, language, session_id, user_id, chat_history, user_profile)` contract
- `AI_SERVICE_URL`, `AI_SERVICE_ENABLED` config
- Fallback to mock when AI is disabled

### For WhatsApp
- Webhook URL: `https://<host>/webhooks/whatsapp`
- Twilio credentials in env
- Idempotent handling of duplicate webhooks (optional)

---

## 7. Phase Status Overview

| Phase | Components | Backend Status | Blocked By |
|-------|------------|----------------|------------|
| 1. Input | Web, WhatsApp, API | Γ£à Done | ΓÇö |
| 2. Processing | Chat, voice, S3 | Γ£à Done | ΓÇö |
| 3. Orchestration | Intent, schemes, eligibility, skills | Γ£à Done | ΓÇö |
| 3. Agents | LangGraph, RAG, DocBridge, Bhasha | ΓÜá∩╕Å Partial | AI team |
| 4. Output | JSON, WhatsApp, MP3 | Γ£à Done | ΓÇö |
| 4. UI | Next.js screens | ΓÇö | Frontend team |
