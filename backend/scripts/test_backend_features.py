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
    r = client.get("/api/schemes/99999")
    assert r.status_code == 404
    r2 = client.get("/api/schemes/1")
    if r2.status_code == 200:
        d = r2.json()
        assert "name" in d and "description" in d and "benefits" in d and "eligibility_rules" in d
        print("GET /api/schemes/1 -> OK (scheme detail)")
    else:
        print("GET /api/schemes/{id} -> OK (endpoint exists, 404 when not found)")


def main():
    print("Testing backend features...\n")
    try:
        test_root()
        test_health()
        test_health_db()
        test_health_dynamo()
        test_chat()
        test_schemes_list()
        test_schemes_detail()
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
