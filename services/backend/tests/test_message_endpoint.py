from fastapi.testclient import TestClient

from backend.api import app

client = TestClient(app)


def test_message_endpoint(setup_test_db):
    resp = client.post(
        "/message",
        json={"user_id": 123, "text": "Hello"},
    )

    # Check
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"reply": "Hello Hello Hello"}
