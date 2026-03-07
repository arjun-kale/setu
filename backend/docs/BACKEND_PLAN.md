# Backend build plan — Rural AI Assistant

We build in phases: **DB + AWS first**, then **APIs that don’t need Twilio/Google**, then **Twilio + voice/STT** later.

---

## Phase 1: Current (.env + DB) — do first

- [x] `.env` with AWS, Postgres, S3 (Twilio / Google STT optional, can be empty)
- [ ] **PostgreSQL schema**: tables for government schemes + eligibility rules
- [ ] **Migrations / create tables** in DB `SETU-AI`
- [ ] **Health + DB check**: e.g. `GET /health` and optional `GET /health/db` that hits Postgres

**Deliverable:** App runs, DB is set up and reachable, no Twilio/Google required.

---

## Phase 2: Core backend (no Twilio, no Google STT)

- [ ] **DynamoDB**: tables for sessions + chat history (create tables, client in code)
- [ ] **S3**: upload/list/delete helpers for audio bucket
- [ ] **Scheme discovery API**: search schemes (PostgreSQL), optional RAG later
- [ ] **Eligibility API**: input (age, income, state, occupation) → eligible schemes (PostgreSQL rules)
- [ ] **Chat API**: session + message handling (DynamoDB), placeholder or simple AI reply (no LangGraph yet)
- [ ] **API docs** and basic error handling

**Deliverable:** Web app can use scheme discovery, eligibility, and chat; no WhatsApp, no voice yet.

---

## Phase 3: Twilio + Google STT (later)

- [ ] Add Twilio + Google STT keys to `.env`
- [ ] **WhatsApp webhook**: receive Twilio events, link to chat/session, reply via Twilio
- [ ] **Voice pipeline**: Google STT, Polly TTS, S3 for audio; voice API endpoint
- [ ] **AI agent**: LangGraph + Pinecone RAG when ready

**Deliverable:** WhatsApp and voice working; full stack as per PROJECT_CONTEXT.

---

## Order of work (summary)

1. **Now:** DB schema + migrations, health with DB check, then Phase 2 tasks.
2. **Later:** Twilio keys + WhatsApp webhook; Google STT + voice; then AI/RAG.

Twilio and Google STT stay optional in config until Phase 3.
