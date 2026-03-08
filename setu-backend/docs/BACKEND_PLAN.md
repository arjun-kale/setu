# Backend Plan — Phased Implementation

## Phase 1 ✓ (Done)

- [x] FastAPI app, config, CORS
- [x] PostgreSQL models and tables (schemes, eligibility)
- [x] DynamoDB (legacy + service: users, sessions, messages)
- [x] Health APIs: `/health`, `/health/db`, `/health/dynamo`
- [x] Chat API: `POST /api/chat`
- [x] Scheme discovery: `GET /api/schemes`, `GET /api/schemes/{id}`
- [x] Eligibility: `POST /api/check-eligibility`
- [x] Voice API: `POST /api/voice` (Whisper STT, Polly TTS)

## Phase 2 (Next) — See `docs/BUILD_PLAN.md`

1. [x] Intent detection (chat / scheme_search / eligibility_check)
2. [x] S3 audio storage
3. [x] Auth (login/register)
4. [x] Skill learning flow
5. [x] Twilio WhatsApp webhook **(last)**

## Excluded (Friend's Work)

- [ ] LangGraph + RAG (Pinecone) — friend will integrate
