# Backend Work ΓÇö Step-by-Step Plan

Clear order of tasks. We can start working through these one by one.

---

## Step 1: Add AI Service Config
**Files:** `app/config/settings.py`, `.env.example`

- Add `AI_SERVICE_URL` (optional, for AI endpoint)
- Add `AI_SERVICE_ENABLED` (default `false` ΓÇö use mock)
- Add `AI_SERVICE_TIMEOUT_SEC` (default `30`)

**Why:** Backend is ready for AI integration; no code change when AI team goes live.

---

## Step 2: Create AI Integration Contract Doc
**File:** `docs/AI_INTEGRATION_CONTRACT.md`

- Document input: `message`, `language`, `session_id`, `user_id`, `chat_history`, `user_profile`
- Document output: plain text string
- Document `chat_history` format
- Document `user_profile` format
- Add example request/response
- Add error handling (timeout ΓåÆ fallback)

**Why:** AI team has a clear contract; fewer integration issues.

---

## Step 3: Pass User Profile to `get_ai_response`
**Files:** `app/services/message_handler.py`, `app/services/ai_agent.py`

- Fetch `user_profile` from DynamoDB in `message_handler`
- Add `user_profile` parameter to `get_ai_response()`
- Pass it when calling `get_ai_response`

**Why:** AI can use age, income, state, occupation for personalized replies.

---

## Step 4: Refactor `ai_agent.py` for Pluggable AI
**File:** `app/services/ai_agent.py`

- When `AI_SERVICE_ENABLED=true` and `AI_SERVICE_URL` is set:
  - HTTP POST to AI service with `{message, language, session_id, user_id, chat_history, user_profile}`
  - Return response text
- When disabled or error:
  - Use mock (current behavior)
- Handle timeout and 5xx gracefully

**Why:** Backend can switch to real AI by changing config; no code change.

---

## Step 5: Add Health Check for AI Service (Optional)
**File:** `app/routes/health.py`

- Add `GET /health/ai`
- When `AI_SERVICE_ENABLED=true` and `AI_SERVICE_URL` set: call AI service and report status
- Else: report "disabled"

**Why:** Ops can monitor AI service health.

---

## Step 6: Add Scheme Summary Endpoint (Optional)
**File:** `app/routes/schemes.py`

- Add `GET /api/schemes/summary` ΓÇö returns lightweight list (id, name, short desc)
- Only if AI team needs it for RAG context

**Why:** AI team can fetch scheme summaries for context without full schema.

---

## Summary

| Step | Task | Priority |
|------|------|----------|
| 1 | Add AI config | High |
| 2 | Create AI_INTEGRATION_CONTRACT.md | High |
| 3 | Pass user_profile to get_ai_response | High |
| 4 | Refactor ai_agent.py for HTTP call | High |
| 5 | Add GET /health/ai | Optional |
| 6 | Add GET /api/schemes/summary | Optional |

**Start with Steps 1ΓÇô4.** Steps 5ΓÇô6 can be done later if needed.
