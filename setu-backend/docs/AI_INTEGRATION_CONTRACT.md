# AI Integration Contract

Contract between the **Setu Backend** and the **AI service** (LangGraph/RAG). The backend calls the AI service when `AI_SERVICE_ENABLED=true`.

---

## 1. Endpoint

| Method | Path | Purpose |
|--------|------|---------|
| POST | `{AI_SERVICE_URL}/chat` | Generate AI response for user message |

**Example:** If `AI_SERVICE_URL=https://ai-service.example.com`, backend calls `POST https://ai-service.example.com/chat`.

---

## 2. Request Format

**Content-Type:** `application/json`

```json
{
  "message": "What schemes are available for farmers?",
  "language": "en",
  "session_id": "whatsapp:+919923410767",
  "user_id": "whatsapp:+919923410767",
  "chat_history": [
    {
      "role": "user",
      "content": "Hello",
      "created_at": "1709876543"
    },
    {
      "role": "assistant",
      "content": "Thanks for your message. How can I help?",
      "created_at": "1709876544"
    }
  ],
  "user_profile": {
    "user_id": "whatsapp:+919923410767",
    "age": 25,
    "income": 150000,
    "state": "MH",
    "occupation": "farmer",
    "updated_at": "1709876500"
  }
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | Current user message |
| `language` | string | Yes | Language code (e.g. `en`, `hi`, `mr`) |
| `session_id` | string | Yes | Session identifier (often same as user_id) |
| `user_id` | string | Yes | User identifier (e.g. `whatsapp:+91999...` or `web-user-123`) |
| `chat_history` | array | Yes | Recent messages (user + assistant), chronological. May be empty `[]` |
| `user_profile` | object \| null | No | User profile if available. `null` if no profile |

### chat_history Item Format

```json
{
  "role": "user" | "assistant",
  "content": "message text",
  "created_at": "unix timestamp as string"
}
```

### user_profile Format

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | string | User ID |
| `age` | int \| null | Age in years |
| `income` | float \| null | Annual income |
| `state` | string \| null | State code (e.g. MH, KA) |
| `occupation` | string \| null | Occupation (e.g. farmer, student) |
| `updated_at` | string | Last update timestamp |

---

## 3. Response Format

**Success (200 OK):**

**Content-Type:** `application/json`

```json
{
  "response": "Here are some schemes for farmers: 1. PM-Kisan..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `response` | string | Plain text response to send to user |

**Alternative:** AI service may return plain text body with `Content-Type: text/plain`. Backend accepts both.

---

## 4. Error Handling

| Scenario | Backend Behavior |
|----------|------------------|
| AI service timeout | Fallback to mock response |
| AI service 5xx | Fallback to mock response |
| AI service 4xx | Fallback to mock response |
| AI service unreachable | Fallback to mock response |
| AI_SERVICE_ENABLED=false | Use mock; never call AI |
| AI_SERVICE_URL empty | Use mock; never call AI |

---

## 5. Example cURL

```bash
curl -X POST "https://ai-service.example.com/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "language": "en",
    "session_id": "test-session",
    "user_id": "test-user",
    "chat_history": [],
    "user_profile": null
  }'
```

**Expected response:**
```json
{"response": "Hello! How can I help you today?"}
```

---

## 6. Backend Config

| Env Variable | Default | Description |
|--------------|---------|-------------|
| `AI_SERVICE_URL` | (empty) | Base URL of AI service (e.g. `https://ai.example.com`) |
| `AI_SERVICE_ENABLED` | `false` | Set `true` to call AI; `false` uses mock |
| `AI_SERVICE_TIMEOUT_SEC` | `30` | Request timeout in seconds |

---

## 7. Summary

- **Backend calls:** `POST {AI_SERVICE_URL}/chat` with JSON body
- **AI returns:** `{"response": "..."}` or plain text
- **On error:** Backend falls back to mock
