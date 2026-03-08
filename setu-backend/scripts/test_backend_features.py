"""
Test all backend features built so far.
Run from backend dir: python scripts/test_backend_features.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "service" in data and "version" in data and "health" in data
    print("GET /          -> OK")


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "healthy"
    assert "version" in data
    print("GET /health    -> OK")


def test_health_db():
    r = client.get("/health/db")
    assert r.status_code == 200
    data = r.json()
    assert "database" in data
    status = "ok" if data["database"] == "ok" else "degraded"
    print(f"GET /health/db -> {status} (database: {data['database'][:50]}...)")


def test_health_dynamo():
    r = client.get("/health/dynamo")
    assert r.status_code == 200
    data = r.json()
    assert "dynamodb" in data
    status = "ok" if data["dynamodb"] == "ok" else "degraded"
    print(f"GET /health/dynamo -> {status} (dynamodb: {data['dynamodb'][:50]}...)")


def test_chat():
    r = client.post(
        "/api/chat",
        json={"user_id": "test-user-001", "message": "Hello", "language": "en"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "response" in data
    assert "session_id" in data
    assert data["session_id"] == "test-user-001"
    assert len(data["response"]) > 0
    print("POST /api/chat  -> OK (response + session_id)")


def test_schemes_list():
    r = client.get("/api/schemes")
    assert r.status_code == 200
    data = r.json()
    assert "schemes" in data
    assert isinstance(data["schemes"], list)
    print("GET /api/schemes -> OK (schemes list)")


def test_schemes_detail():
    r = client.get("/api/schemes/1")
    if r.status_code == 200:
        d = r.json()
        assert "name" in d and "description" in d and "benefits" in d and "eligibility_rules" in d
        print("GET /api/schemes/1 -> OK (scheme detail)")
    else:
        print("GET /api/schemes/1 -> OK (or 404 if no data)")


def test_schemes_404():
    """GET /api/schemes/{id} returns 404 when scheme not found."""
    r = client.get("/api/schemes/99999")
    assert r.status_code == 404
    assert "not found" in r.json().get("detail", "").lower()
    print("GET /api/schemes/99999 -> OK (404 Not Found)")


def test_check_eligibility():
    r = client.post(
        "/api/check-eligibility",
        json={"age": 25, "income": 100000, "state": "MH", "occupation": "farmer"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "schemes" in data
    assert isinstance(data["schemes"], list)
    print("POST /api/check-eligibility -> OK (schemes list)")


def test_chat_scheme_intent():
    """Chat with scheme_search intent returns scheme list."""
    r = client.post(
        "/api/chat",
        json={"user_id": "test-intent-1", "message": "What schemes are available for farmers?", "language": "en"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "response" in data
    # Should get scheme search result (list or "no schemes")
    assert len(data["response"]) > 0
    print("POST /api/chat (scheme intent) -> OK")


def test_chat_eligibility_intent():
    """Chat with eligibility_check intent returns helpful message or schemes."""
    r = client.post(
        "/api/chat",
        json={"user_id": "test-intent-2", "message": "Am I eligible for any scheme?", "language": "en"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "response" in data
    assert len(data["response"]) > 0
    print("POST /api/chat (eligibility intent) -> OK")


def test_schemes_search():
    """GET /api/schemes?q=farmer returns filtered list."""
    r = client.get("/api/schemes?q=farmer")
    assert r.status_code == 200
    data = r.json()
    assert "schemes" in data
    assert isinstance(data["schemes"], list)
    print("GET /api/schemes?q=farmer -> OK")


def test_auth_register_login():
    """Register and login return token."""
    import uuid
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    r = client.post("/api/auth/register", json={"email": email, "password": "test123", "name": "Test"})
    assert r.status_code == 200
    data = r.json()
    assert "token" in data and data["email"] == email
    r2 = client.post("/api/auth/login", json={"email": email, "password": "test123"})
    assert r2.status_code == 200
    assert "token" in r2.json()
    print("POST /api/auth/register, /api/auth/login -> OK")


def test_auth_login_invalid():
    """Login with wrong password returns 401."""
    r = client.post("/api/auth/login", json={"email": "nonexistent@x.com", "password": "wrong"})
    assert r.status_code == 401
    print("POST /api/auth/login (invalid) -> OK (401)")


def test_skills_list():
    """GET /api/skills returns learning topics."""
    r = client.get("/api/skills")
    assert r.status_code == 200
    data = r.json()
    assert "skills" in data and len(data["skills"]) > 0
    print("GET /api/skills -> OK")


def test_skills_detail():
    """GET /api/skills/1 returns one skill."""
    r = client.get("/api/skills/1")
    assert r.status_code == 200
    data = r.json()
    assert "title" in data and "content" in data
    print("GET /api/skills/1 -> OK")


def test_skills_404():
    """GET /api/skills/{id} returns 404 when skill not found."""
    r = client.get("/api/skills/99999")
    assert r.status_code == 404
    assert "not found" in r.json().get("detail", "").lower()
    print("GET /api/skills/99999 -> OK (404 Not Found)")


def test_chat_skill_intent():
    """Chat with skill_learning intent returns skill content."""
    r = client.post(
        "/api/chat",
        json={"user_id": "test-skill", "message": "I want to learn digital skills", "language": "en"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "response" in data and len(data["response"]) > 0
    print("POST /api/chat (skill intent) -> OK")


def test_update_profile():
    """PUT /api/users/{user_id}/profile updates profile."""
    r = client.put(
        "/api/users/test-profile-user/profile",
        json={"age": 30, "income": 150000, "state": "MH", "occupation": "farmer"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "Profile updated" in data.get("message", "")
    print("PUT /api/users/{id}/profile -> OK")


def test_chat_history():
    """GET /api/chat/history returns messages for a session."""
    # First send a message to create history
    client.post(
        "/api/chat",
        json={"user_id": "test-history-user", "message": "Hello", "language": "en"},
    )
    r = client.get("/api/chat/history", params={"session_id": "test-history-user"})
    assert r.status_code == 200
    data = r.json()
    assert "session_id" in data and data["session_id"] == "test-history-user"
    assert "messages" in data and isinstance(data["messages"], list)
    assert len(data["messages"]) >= 2  # user + assistant
    print("GET /api/chat/history -> OK")


def test_whatsapp_webhook():
    """POST /webhooks/whatsapp accepts Twilio webhook format."""
    r = client.post(
        "/webhooks/whatsapp",
        data={"From": "whatsapp:+919999999999", "Body": "Hello"},
    )
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
    print("POST /webhooks/whatsapp -> OK")


def test_invalid_route_404():
    """Unknown route returns 404."""
    r = client.get("/api/nonexistent-endpoint-xyz")
    assert r.status_code == 404
    print("GET /api/nonexistent -> OK (404 Not Found)")


def test_voice_empty():
    """POST /api/voice with empty audio returns 400."""
    r = client.post(
        "/api/voice",
        files={"audio": ("empty.wav", b"", "audio/wav")},
        data={"user_id": "test-voice", "language": "en-IN"},
    )
    assert r.status_code == 400
    assert "empty" in r.json().get("detail", "").lower() or "Empty" in str(r.json())
    print("POST /api/voice (empty) -> OK (400 as expected)")


def main():
    print("Testing backend features...\n")
    try:
        test_root()
        test_health()
        test_health_db()
        test_health_dynamo()
        test_chat()
        test_chat_scheme_intent()
        test_chat_eligibility_intent()
        test_schemes_list()
        test_schemes_search()
        test_schemes_detail()
        test_schemes_404()
        test_check_eligibility()
        test_auth_register_login()
        test_auth_login_invalid()
        test_skills_list()
        test_skills_detail()
        test_skills_404()
        test_chat_skill_intent()
        test_update_profile()
        test_chat_history()
        test_whatsapp_webhook()
        test_voice_empty()
        test_invalid_route_404()
        print("\nAll feature checks passed.")
        return 0
    except AssertionError as e:
        print(f"\nFAIL: {e}")
        return 1
    except Exception as e:
        print(f"\nERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
