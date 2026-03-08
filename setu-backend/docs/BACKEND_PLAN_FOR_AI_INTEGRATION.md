# Backend Plan ΓÇö Preparation for RAG/LangGraph Integration

**Scope:** Backend work only. RAG and LangGraph implementation is assigned to another team.

**Goal:** Prepare the backend so that when the AI team integrates RAG/LangGraph, everything connects smoothly with minimal changes.

---

## 1. Integration Point (AI Team Will Replace)

The AI team will replace **one function** in the backend:

| File | Function | Current | After Integration |
|------|----------|---------|-------------------|
| `app/services/ai_agent.py` | `get_ai_response()` | Mock responses | Call LangGraph/RAG service |

**Interface (must stay stable):**

```python
def get_ai_response(
    message: str,
    language: str = "en",
    *,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    chat_history: Optional[list[dict[str, Any]]] = None,
) -> str:
    """Returns response text. Input/output contract must not change."""
```

---

## 2. Backend Tasks (Our Work)

### 2.1 Add AI Service Config (Placeholder for AI Team)

**Task:** Add env variables for the future AI service so deployment is ready.

| Variable | Purpose | Example |
|----------|---------|---------|
| `AI_SERVICE_URL` | LangGraph/RAG API endpoint | `http://localhost:8001` or `https://ai-service.xxx` |
| `AI_SERVICE_ENABLED` | Toggle: use real AI or mock | `false` (mock) ΓåÆ `true` (real) |
| `AI_SERVICE_TIMEOUT_SEC` | Request timeout | `30` |

**File:** `app/config/settings.py`, `.env.example`

---

### 2.2 Document Chat History Format (For AI Team)

**Task:** Document the exact format of `chat_history` passed to `get_ai_response`.

**Format (current):**
```python
[
    {"role": "user", "content": "What schemes for farmers?", "created_at": "..."},
    {"role": "assistant", "content": "1. PM-Kisan...", "created_at": "..."},
]
```

**File:** Add to `docs/AI_INTEGRATION_CONTRACT.md`

---

### 2.3 Document User Profile Format (For AI Team)

**Task:** Document user profile structure so AI can use it for context.

**Format:**
```python
{
    "user_id": "whatsapp:+91999...",
    "age": 25,
    "income": 150000,
    "state": "MH",
    "occupation": "farmer",
    "updated_at": "..."
}
```

**Access:** `dynamo.get_user_profile(user_id)` ΓÇö AI team can receive this if we pass it.

---

### 2.4 Expose Scheme Data for AI Context (Optional)

**Task:** Provide a helper or API so the AI service can fetch scheme summaries for RAG context.

**Options:**
- **A:** Keep as-is ΓÇö AI team builds their own RAG from PostgreSQL or a separate pipeline.
- **B:** Add `GET /api/schemes/summary` ΓÇö returns lightweight scheme list (id, name, short desc) for AI to use.

**Recommendation:** A is fine. Backend already has `GET /api/schemes` and `search_schemes()`. AI team can call these or ingest separately.

---

### 2.5 Refactor `ai_agent.py` for Pluggable Implementation

**Task:** Make `get_ai_response` call an external service when `AI_SERVICE_ENABLED=true`.

**Logic:**
```
if AI_SERVICE_ENABLED and AI_SERVICE_URL:
    ΓåÆ HTTP POST to AI_SERVICE_URL with {message, language, session_id, user_id, chat_history, user_profile}
    ΓåÆ Return response text
else:
    ΓåÆ Use mock (current behavior)
```

**File:** `app/services/ai_agent.py`

**Benefit:** AI team deploys their service; backend just flips a config. No code change in backend when they go live.

---

### 2.6 Pass User Profile to `get_ai_response`

**Task:** Include user profile in the context passed to AI.

**Current:** `get_ai_response(message, language, session_id, user_id, chat_history)`

**Add:** `user_profile: Optional[dict] = None`

**File:** `app/services/message_handler.py`, `app/services/ai_agent.py`

**Benefit:** AI can use age, income, state, occupation for personalized responses.

---

### 2.7 Add AI Integration Contract Doc

**Task:** Create `docs/AI_INTEGRATION_CONTRACT.md` with:

- Input schema (message, language, session_id, user_id, chat_history, user_profile)
- Output schema (plain text string)
- Error handling (timeout, 5xx ΓåÆ fallback to mock or generic message)
- Example request/response

**Benefit:** AI team has a clear contract; no back-and-forth.

---

### 2.8 Health Check for AI Service (Optional)

**Task:** Add `GET /health/ai` ΓÇö checks if AI service is reachable when `AI_SERVICE_ENABLED=true`.

**File:** `app/routes/health.py`

**Benefit:** Ops can monitor AI service health.

---

## 3. What Backend Will NOT Do

| Item | Owner |
|------|-------|
| LangGraph implementation | AI team |
| RAG (Pinecone/Kendra) | AI team |
| Vector embeddings | AI team |
| Agent orchestration | AI team |
| Document AI (DocBridge) | AI team |
| Bhasha (language/dialect) | AI team |

---

## 4. Implementation Order

| # | Task | Effort | Priority |
|---|------|--------|----------|
| 1 | Add AI config (AI_SERVICE_URL, AI_SERVICE_ENABLED, timeout) | Low | High |
| 2 | Create AI_INTEGRATION_CONTRACT.md | Low | High |
| 3 | Pass user_profile to get_ai_response | Low | High |
| 4 | Refactor ai_agent.py for HTTP call when AI enabled | Medium | High |
| 5 | Add GET /health/ai (optional) | Low | Medium |
| 6 | Add GET /api/schemes/summary (optional, if AI team needs) | Low | Low |

---

## 5. Summary

**Backend responsibilities:**
- Keep `get_ai_response` interface stable
- Add config for AI service URL and enable flag
- Pass user_profile + chat_history in the format documented
- Call AI service via HTTP when enabled; fallback to mock otherwise
- Document the contract for the AI team

**AI team responsibilities:**
- Build LangGraph + RAG service
- Expose HTTP endpoint that accepts our request format
- Return plain text response
- Handle timeouts/errors gracefully

**Integration flow (after AI team is ready):**
1. Set `AI_SERVICE_ENABLED=true`, `AI_SERVICE_URL=https://...` in .env
2. Backend calls AI service instead of mock
3. No other backend code changes needed
