# Backend Plan — Phased Implementation

## Phase 1 ✓ (Done)

- [x] FastAPI app, config, CORS
- [x] PostgreSQL models and tables (schemes, eligibility)
- [x] DynamoDB (legacy + service: users, sessions, messages)
- [x] Health APIs: `/health`, `/health/db`, `/health/dynamo`
- [x] Chat API: `POST /api/chat`
- [x] Scheme discovery: `GET /api/schemes`, `GET /api/schemes/{id}`
- [x] Eligibility: `POST /api/check-eligibility`

## Phase 2 (Next)

- [ ] Intent detection in chat
- [ ] S3 usage for audio
- [ ] Full chat flow with AI agent

## Phase 3 (Planned)

- [ ] Twilio WhatsApp webhook
- [ ] Voice pipeline (STT/TTS)
- [ ] AI/RAG (LangGraph + Pinecone)
