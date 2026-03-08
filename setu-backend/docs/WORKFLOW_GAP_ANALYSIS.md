# Workflow Gap Analysis ΓÇö Diagram vs Current Backend

Comparison of the target workflow diagram with the current Setu backend implementation.

---

## 1. Architecture Difference

| Aspect | Workflow Diagram | Current Backend |
|--------|------------------|-----------------|
| **Compute** | AWS Lambda (serverless) | FastAPI (single server) |
| **Orchestration** | LangGraph Python Agents | Rule-based `message_handler` |
| **Voice queue** | SQS (async) | Synchronous (no queue) |
| **Agents** | Multiple specialized agents | Single `process_message` + mock AI |

---

## 2. Component-by-Component Comparison

### Γ£à Implemented (Matches or Covers Diagram)

| Diagram Component | Current Implementation | Status |
|-------------------|-------------------------|--------|
| **User (Web PWA / WhatsApp)** | Supported via web + Twilio | Γ£à |
| **WhatsApp Bot (Twilio Webhook)** | `POST /webhooks/whatsapp` | Γ£à |
| **API Route (api/voice/, api/chat/)** | `POST /api/chat`, `POST /api/voice` | Γ£à |
| **S3 (Audio Storage)** | `s3_client.py` ΓÇö uploads voice input/output | Γ£à |
| **DynamoDB (Memory + User Profile)** | `dynamodb_service.py` ΓÇö users, sessions, messages, user_profiles | Γ£à |
| **TTS (Polly)** | `voice_service.py` ΓÇö Amazon Polly | Γ£à |
| **S3 (Audio Response)** | Voice output uploaded to S3 | Γ£à |
| **Scheme search** | `scheme_service.py` + PostgreSQL | Γ£à (PostgreSQL, not Pinecone) |
| **Eligibility check** | `eligibility_service.py` | Γ£à |
| **Skills** | `skill_service.py` ΓÇö static content | Γ£à (simplified vs Siriwani Agent) |

### ΓÜá∩╕Å Partially Implemented

| Diagram Component | Current State | Gap |
|-------------------|---------------|-----|
| **Lambda chat-process** | FastAPI routes handle directly (no Lambda) | Different architecture ΓÇö FastAPI does the job |
| **Lambda voice-ingest** | Voice handled in `POST /api/voice` | No Lambda, no SQS ΓÇö synchronous |
| **Python Agents (LangGraph Orchestrator)** | `message_handler` + `intent_detection` | Rule-based routing, not LangGraph |
| **Scheme Compass Agent (RAG)** | PostgreSQL keyword search | No Pinecone/Kendra, no RAG |
| **Siriwani Agent (Skills + Quiz)** | Static skills content | No quiz, no agent structure |

### Γ¥î Not Implemented

| Diagram Component | Status |
|-------------------|--------|
| **Lambda whatsapp-webhook** | N/A ΓÇö FastAPI webhook instead |
| **Lambda voice-ingest** | N/A ΓÇö FastAPI handles voice |
| **SQS (Voice Queue)** | Not used ΓÇö synchronous processing |
| **DocBridge Agent (Document AI)** | Not implemented |
| **Google DocumentAI** | Not integrated |
| **Pinecone / Kendra (Scheme Search)** | Not used ΓÇö PostgreSQL only |
| **Bhasha Agent (Language + Dialect)** | Not implemented |
| **LangGraph Orchestrator** | Mock AI only ΓÇö no real orchestrator |
| **Quiz (in Siriwani)** | Not implemented |

---

## 3. Data Flow Comparison

### Diagram Flow
```
User ΓåÆ WhatsApp/Twilio ΓåÆ Lambda whatsapp-webhook ΓåÆ Lambda chat-process
User ΓåÆ API ΓåÆ Lambda voice-ingest ΓåÆ S3 + SQS ΓåÆ Lambda chat-process
                                                    Γåô
                                    Python Agents (LangGraph)
                                                    Γåô
                    DocBridge | Siriwani | Scheme Compass | Bhasha | DynamoDB | TTS
                                                    Γåô
                                    Next.js ΓåÆ User UI
```

### Current Flow
```
User ΓåÆ WhatsApp ΓåÆ POST /webhooks/whatsapp ΓåÆ message_handler.process_message()
User ΓåÆ Web ΓåÆ POST /api/chat ΓåÆ message_handler.process_message()
User ΓåÆ Web ΓåÆ POST /api/voice ΓåÆ STT ΓåÆ process_message() ΓåÆ TTS ΓåÆ S3
                                                    Γåô
                                    intent_detection ΓåÆ scheme_search | eligibility | skill_learning | chat
                                                    Γåô
                                    PostgreSQL | DynamoDB | skill_service | ai_agent (mock)
                                                    Γåô
                                    Response (JSON or Twilio or MP3)
```

---

## 4. What's Remaining to Match the Diagram

### High Priority

| Item | Description |
|------|-------------|
| **LangGraph + Python Agents** | Replace mock AI with LangGraph orchestrator |
| **Pinecone/Kendra for scheme RAG** | Add vector search for schemes (or keep PostgreSQL if sufficient) |
| **Real AI chat** | Replace `get_ai_response` mock with LangGraph |

### Medium Priority

| Item | Description |
|------|-------------|
| **Bhasha Agent** | Language/dialect detection and translation |
| **DocBridge Agent** | Document AI (e.g. Aadhaar, form upload) via Google DocumentAI |
| **Siriwani Agent (Quiz)** | Add quiz flow to skills |
| **SQS for voice** | Optional: async voice processing |

### Lower Priority (Architecture)

| Item | Description |
|------|-------------|
| **Lambda migration** | Move from FastAPI to Lambda (optional ΓÇö FastAPI works) |
| **Serverless** | Diagram assumes serverless; current is monolithic |

---

## 5. Summary

| Category | Count |
|----------|-------|
| Γ£à Fully implemented | 10 |
| ΓÜá∩╕Å Partially implemented | 5 |
| Γ¥î Not implemented | 9 |

**Core flow works:** WhatsApp, chat, voice, schemes, eligibility, skills, DynamoDB, S3, Polly ΓÇö all functional.

**Main gaps:** LangGraph orchestrator, Pinecone/Kendra RAG, DocBridge (Document AI), Bhasha (language), and quiz in skills.

---

## 6. Recommended Next Steps

1. **Integrate LangGraph** ΓÇö Replace `ai_agent.py` mock with LangGraph orchestrator.
2. **Add Pinecone/Kendra** ΓÇö Optional RAG for scheme search (or keep PostgreSQL).
3. **Bhasha Agent** ΓÇö Add language/dialect handling for multi-language support.
4. **DocBridge Agent** ΓÇö Add document upload and Google DocumentAI for forms/Aadhaar.
5. **Quiz in skills** ΓÇö Extend Siriwani flow with quiz logic.
