# Rural AI Assistant — Application Workflow

This document is the **single source of truth** for backend API implementation. Use it for step-by-step feature implementation.

---

## System Purpose

A **multilingual AI assistant** that helps citizens:
- Discover government schemes  
- Check eligibility  
- Learn skills  
- Complete digital tasks  

using **chat** or **voice**.

**Access channels:** Web application | WhatsApp

---

## Backend Architecture (Summary)

| Component | Role |
|-----------|------|
| **FastAPI** | Handles all requests (web + WhatsApp webhook) |
| **DynamoDB** | user sessions, chat history, user profiles |
| **PostgreSQL** | government schemes, eligibility rules, scheme documentation |
| **Amazon S3** | audio files |
| **Google Speech-to-Text** | voice → text |
| **Amazon Polly** | text → speech |
| **Twilio** | WhatsApp API |
| **LangGraph + Pinecone RAG** | AI agents |

---

## Main Application Workflow (Chat / Text)

```
Step 1   User sends message (web or WhatsApp)
              │
              ▼
Step 2   Request reaches FastAPI backend
              │
              ▼
Step 3   Backend checks user session in DynamoDB
              │
              ▼
Step 4   Backend performs INTENT DETECTION
         Request type is one of:
         • chat
         • scheme_search
         • eligibility_check
         • skill_learning
              │
              ▼
Step 5   Branch by intent:
         ┌─────────────────────────────────────────────────────────────┐
         │ scheme_search    → Query PostgreSQL schemes (and related)     │
         │ eligibility_check → Query PostgreSQL scheme_eligibility       │
         │ chat              → Send to AI agent system                  │
         │ skill_learning    → (handled via AI / specific flow)         │
         └─────────────────────────────────────────────────────────────┘
              │
              ▼
Step 6   AI agents (when used) retrieve context from:
         • Pinecone vector database (RAG)
         • PostgreSQL scheme data
         • DynamoDB user memory / chat history
              │
              ▼
Step 7   AI generates response
              │
              ▼
Step 8   Response stored in DynamoDB chat history
              │
              ▼
Step 9   Backend returns response to frontend or WhatsApp
```

---

## Intent Types (for API design)

| Intent | Backend action | Data source |
|--------|----------------|-------------|
| **chat** | Send to AI agent; use RAG + user memory | Pinecone, PostgreSQL, DynamoDB |
| **scheme_search** | Search/browse schemes | PostgreSQL (schemes, scheme_documents) |
| **eligibility_check** | Match user profile to schemes | PostgreSQL (schemes, scheme_eligibility) |
| **skill_learning** | Learning content / tasks | AI agent or dedicated flow |

---

## Voice Workflow

```
User uploads voice message
        │
        ▼
Backend receives audio
        │
        ▼
Backend sends audio to Google Speech-to-Text
        │
        ▼
Speech converted to TEXT
        │
        ▼
Text sent into main flow (Step 2–9) as user message
(e.g. intent detection → scheme_search / eligibility_check / chat / skill_learning)
        │
        ▼
AI response generated (text)
        │
        ▼
Backend converts text to speech using Amazon Polly
        │
        ▼
Audio stored in S3 (if needed) and/or streamed
        │
        ▼
Audio returned to user (web or WhatsApp)
```

---

## Backend APIs to Implement (from workflow)

1. **Unified entry**
   - Web: e.g. `POST /api/v1/messages` (session_id, message, channel=web).
   - WhatsApp: `POST /webhooks/whatsapp` (Twilio payload) → same logic with channel=whatsapp.

2. **Session**
   - Get or create session (DynamoDB) from request (user/session id, channel).

3. **Intent detection**
   - Input: user message (and optionally session history).
   - Output: one of `chat` | `scheme_search` | `eligibility_check` | `skill_learning`.
   - Can be rule-based first, then model-based.

4. **Scheme search**
   - Input: query (and filters).
   - Action: query PostgreSQL schemes (and scheme_documents).
   - Output: list of matching schemes.

5. **Eligibility check**
   - Input: user profile (age, income, state, occupation, etc.) from DynamoDB or request.
   - Action: query PostgreSQL scheme_eligibility (and schemes).
   - Output: list of eligible schemes (and optionally why others are not).

6. **Chat (AI)**
   - Input: message + session_id.
   - Action: LangGraph agent with Pinecone RAG + PostgreSQL + DynamoDB context.
   - Output: assistant message; store in DynamoDB chat history.

7. **Voice**
   - `POST /api/v1/voice` (or similar): audio in → Google STT → text → main flow → AI response → Polly → audio out (and optionally S3).

8. **Persistence**
   - Every assistant response: save to DynamoDB chat history (and update session if needed).

---

## Data Flow Summary

| Step | DynamoDB | PostgreSQL | Other |
|------|----------|------------|--------|
| 3 | Read/create session | — | — |
| 5 (scheme_search) | — | Read schemes (scheme_documents) | — |
| 5 (eligibility_check) | Read user profile (optional) | Read scheme_eligibility, schemes | — |
| 5 (chat) | Read chat history | Read schemes if needed | Pinecone RAG |
| 6 | Read user memory / history | Read scheme data | Pinecone |
| 8 | Write chat message | — | — |
| Voice | — | — | S3 (audio), Google STT, Polly |

---

## Implementation order (suggested)

1. **Session + single message endpoint** — get/create session (DynamoDB), accept message, return placeholder response; save message and response in DynamoDB.
2. **Intent detection** — classify message into chat | scheme_search | eligibility_check | skill_learning (simple rules or small model).
3. **Scheme search API** — query PostgreSQL schemes (and scheme_documents); call from main flow when intent = scheme_search.
4. **Eligibility check API** — query scheme_eligibility + schemes; call when intent = eligibility_check; use profile from DynamoDB or request.
5. **Chat (AI) path** — integrate LangGraph + Pinecone RAG; call when intent = chat; read/write DynamoDB.
6. **Skill learning** — define flow and wire to main path.
7. **WhatsApp webhook** — receive Twilio, map to session, run same flow, respond via Twilio.
8. **Voice** — endpoint: audio in → STT → main flow → Polly → audio out; S3 if needed.

If you want to add or change anything at any step (e.g. extra intents, different DB usage), we can update this workflow and then implement accordingly.
