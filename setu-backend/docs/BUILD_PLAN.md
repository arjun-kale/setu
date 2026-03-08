# Backend Build Plan — What's Left (Twilio Last, LangGraph/RAG Excluded)

**Scope:** Backend features we will build.  
**Excluded:** LangGraph + RAG (friend will integrate).  
**Last:** Twilio WhatsApp webhook.

---

## Build Order

| # | Feature | Priority | Description |
|---|---------|----------|-------------|
| 1 | **Intent detection** | High | Route message to chat / scheme_search / eligibility_check | ✅ Done |
| 2 | **S3 audio storage** | Medium | Store voice input/output in S3 (optional) | ✅ Done |
| 3 | **Auth** | Medium | Login/register, JWT or session (if needed) | ✅ Done |
| 4 | **Skill learning flow** | Low | Placeholder or simple flow for learning content | ✅ Done |
| 5 | **Twilio WhatsApp webhook** | Last | `POST /webhooks/whatsapp` → same chat flow | ✅ Done |

---

## 1. Intent Detection (Next)

**Goal:** Classify user message and route to the right handler.

| Intent | Action | API / logic |
|--------|--------|-------------|
| `scheme_search` | Search schemes by keyword | Use existing `GET /api/schemes` + search |
| `eligibility_check` | Check eligibility | Use existing `POST /api/check-eligibility` (need user profile) |
| `chat` | General conversation | Send to AI agent (mock for now; friend adds LangGraph) |
| `skill_learning` | Learning content | Placeholder or simple flow |

**Implementation:**
- Add `app/services/intent_detection.py` — rule-based or keyword-based
- Update chat route: detect intent → branch to scheme search, eligibility, or chat
- Keep AI agent call for `chat` intent (friend will replace with LangGraph + RAG)

---

## 2. S3 Audio Storage (Medium)

**Goal:** Store voice input/output in S3 for audit or replay.

**Implementation:**
- Use existing `s3_client.py`
- On `POST /api/voice`: upload input audio and output MP3 to S3
- Optional: return S3 URLs in response headers

---

## 3. Auth (Medium)

**Goal:** User login/register if required for production.

**Implementation:**
- JWT or session-based auth
- Endpoints: `POST /api/auth/register`, `POST /api/auth/login`
- Protect chat/voice with user token
- Store user in DynamoDB (already have `users` table)

---

## 4. Skill Learning Flow (Low)

**Goal:** Simple flow for learning content.

**Implementation:**
- Placeholder endpoint or redirect to chat with `intent=skill_learning`
- Or static content from DB/JSON

---

## 5. Twilio WhatsApp Webhook (Last)

**Goal:** Receive WhatsApp messages, run same chat flow, reply via Twilio.

**Implementation:**
- `POST /webhooks/whatsapp` — Twilio webhook
- Parse incoming message → detect intent → run chat/scheme/eligibility flow
- Send reply via Twilio API
- Map WhatsApp number to `user_id` in DynamoDB

---

## Excluded (Friend's Work)

| Feature | Owner |
|---------|-------|
| **LangGraph + RAG (Pinecone)** | Friend |

Backend keeps the mock AI agent. Friend will replace `get_ai_response()` with LangGraph + RAG when ready.

---

## Summary

```
1. Intent detection     ← Next
2. S3 audio storage
3. Auth
4. Skill learning
5. Twilio WhatsApp     ← Last
────────────────────────────
   LangGraph + RAG      ← Friend
```
