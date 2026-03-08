# Setu Backend — Current User Workflow & Additional Features

## 1. Current User Workflow

### Overview

Users interact with the Rural AI Assistant through **two channels**: **Web** and **WhatsApp**. Both use the same backend logic — intent detection → scheme search / eligibility / skills / chat.

---

## 2. User Journeys by Channel

### A. WhatsApp User Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. USER JOINS SANDBOX                                                    │
│    User sends "join <keyword>" to Twilio sandbox number                  │
│    Twilio confirms: "You are all set!"                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. USER SENDS MESSAGE                                                    │
│    e.g. "What schemes for farmers?" / "Hello" / "Am I eligible?"        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. TWILIO → BACKEND                                                      │
│    POST /webhooks/whatsapp (From, Body)                                  │
│    Backend: create/ensure user, session in DynamoDB                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. INTENT DETECTION                                                      │
│    Keywords → scheme_search | eligibility_check | skill_learning | chat  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┬───────────────┐
                    ▼               ▼               ▼               ▼
            scheme_search   eligibility_check  skill_learning      chat
                    │               │               │               │
                    ▼               ▼               ▼               ▼
            PostgreSQL        PostgreSQL       Static SKILLS    Mock AI
            scheme search     eligibility      content          response
                    │               │               │               │
                    └───────────────┴───────────────┴───────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. RESPONSE                                                             │
│    Save to DynamoDB → send via Twilio → user receives reply on WhatsApp │
└─────────────────────────────────────────────────────────────────────────┘
```

### B. Web User Flow (Chat API)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. USER OPENS WEB APP                                                   │
│    (Frontend loads; may call GET /health)                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. USER TYPES MESSAGE (or loads history)                               │
│    POST /api/chat {user_id, message, language}                          │
│    GET /api/chat/history?session_id=xxx — load past messages            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. SAME BACKEND FLOW AS WHATSAPP                                        │
│    Intent detection → scheme/eligibility/skill/chat                     │
│    Returns {response, session_id}                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. FRONTEND DISPLAYS RESPONSE                                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### C. Voice User Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. USER RECORDS VOICE                                                   │
│    (Web or mobile app)                                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. FRONTEND UPLOADS AUDIO                                               │
│    POST /api/voice (audio file, user_id, language)                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. SPEECH-TO-TEXT (Whisper or Google)                                   │
│    Audio → transcript (e.g. "What schemes for farmers?")                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. SAME CHAT FLOW                                                        │
│    process_message(transcript) → scheme/eligibility/skill/chat           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. TEXT-TO-SPEECH (Polly)                                               │
│    Response text → MP3 audio                                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 6. S3 UPLOAD + RETURN                                                   │
│    Upload input/output to S3 → return MP3 to user                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### D. Direct API User Flow (Scheme / Eligibility)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SCHEME SEARCH                                                            │
│ GET /api/schemes?q=farmer                                                │
│ → PostgreSQL search → {schemes: [...]}                                   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ ELIGIBILITY CHECK                                                        │
│ POST /api/check-eligibility {age, income, state, occupation}             │
│ → Match against scheme_eligibility → {schemes: [...]}                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Current Workflow Summary

| Step | WhatsApp | Web Chat | Voice |
|------|----------|----------|-------|
| Entry | Twilio webhook | POST /api/chat | POST /api/voice |
| User ID | From (whatsapp:+91...) | user_id in body | user_id in form |
| Intent | Yes | Yes | Yes (after STT) |
| Response | Twilio send | JSON response | MP3 + S3 URLs |
| Storage | DynamoDB | DynamoDB | DynamoDB + S3 |

**Shared logic:** `message_handler.process_message()` + `intent_detection.detect_intent()`

---

## 4. What's Working Today

| Feature | Status | Notes |
|---------|--------|------|
| Scheme search | ✅ | PostgreSQL, keyword search |
| Eligibility check | ✅ | User profile from DynamoDB or request |
| Skill learning | ✅ | Static content (4 topics) |
| Chat (general) | ✅ | Mock AI responses |
| WhatsApp | ✅ | Twilio webhook + reply |
| Voice | ✅ | Whisper STT, Polly TTS, S3 |
| Auth | ✅ | Register, login, JWT |
| User profile | ✅ | Age, income, state, occupation |

---

## 5. Additional Features to Add

### High Priority

| Feature | Description | Effort |
|---------|-------------|--------|
| **Real AI (LangGraph + RAG)** | Replace mock AI with LangGraph + Pinecone for scheme FAQs, context-aware chat | High |
| **JWT-protected routes** | Add `get_current_user` dependency; protect chat, voice, profile | Medium |
| **Multi-language support** | Detect language from message; return responses in Hindi, Marathi, etc. | Medium |
| **Scheme documents** | Link to PDFs/URLs for each scheme; return in search/eligibility | Low |
| **Eligibility "why not"** | Explain why user doesn't qualify for certain schemes | Medium |

### Medium Priority

| Feature | Description | Effort |
|---------|-------------|--------|
| **WhatsApp voice** | Accept voice notes via WhatsApp; STT → chat flow → TTS reply | Medium |
| **Session timeout** | Auto-expire sessions after 24h; clear context | Low |
| **Rate limiting** | Limit requests per user/IP to prevent abuse | Low |
| **Analytics** | Log intents, popular schemes, user counts (DynamoDB or external) | Medium |
| **Admin API** | Add/update schemes, view usage (protected) | Medium |
| **Feedback** | "Was this helpful?" after each response; store in DynamoDB | Low |
| **Reminders** | "Remind me about PM-Kisan in 3 days" → scheduled WhatsApp | High |

### Lower Priority

| Feature | Description | Effort |
|---------|-------------|--------|
| **Skills from DB** | Move skills from code to PostgreSQL or config | Low |
| **ML-based intent** | Replace keyword intent with small classifier | Medium |
| **Conversation memory** | Long-term user preferences (e.g. "I'm a farmer") | Medium |
| **Offline mode** | Cache schemes for low-connectivity | High |
| **Aadhaar/DigiLocker** | Verify identity for scheme applications | High |
| **Application tracking** | Track user's scheme application status | High |
| **Notifications** | Push scheme updates to users who expressed interest | Medium |

### Nice to Have

| Feature | Description |
|---------|-------------|
| **WebSocket chat** | Real-time streaming for web |
| **Voice streaming** | Stream TTS chunks instead of full MP3 |
| **Image/PDF upload** | User uploads document for eligibility check |
| **OTP verification** | Verify phone/email for sensitive actions |
| **Localization** | Full UI + response translation (i18n) |

---

## 6. Recommended Next Steps

1. **Integrate real AI** — LangGraph + Pinecone RAG (as planned)
2. **Add JWT protection** — Protect chat, voice, profile endpoints
3. **Scheme documents** — Add document URLs to scheme responses
4. **Feedback** — Simple thumbs up/down to improve responses
5. **Rate limiting** — Protect against abuse

---

## 7. Workflow Diagram (Simplified)

```
                    ┌──────────────┐
                    │   USER       │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ WhatsApp │ │ Web Chat │ │  Voice   │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             └────────────┼────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  process_message()   │
              │  intent_detection()  │
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   scheme_search   eligibility    skill_learning
         │               │               │
         ▼               ▼               ▼
   PostgreSQL       PostgreSQL      Static
   schemes          eligibility     SKILLS
         │               │               │
         └───────────────┴───────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  chat (AI)            │
              │  → Mock / LangGraph  │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  DynamoDB save        │
              │  Response to user     │
              └──────────────────────┘
```
