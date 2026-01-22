from fastapi.testclient import TestClient
from sqlalchemy import select

from backend.api import app
from backend.db import account_table, message_table, engine

client = TestClient(app)


def test_message_endpoint_saves_message_and_user(setup_test_db):
    # Setup
    _ = setup_test_db

    # Run
    resp = client.post(
        "/message",
        json={"user_id": 123, "text": "Hello"},
    )

    # Check
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"reply": "Hello Hello Hello", "keyboard_type": "main"}

    with engine.connect() as conn:

        message_rows = conn.execute(select(message_table)).all()
        assert len(message_rows) == 1
        message = message_rows[0]
        assert message.id == 1
        assert message.user_id == 123
        assert message.text == "Hello"
        assert message.created_at is not None

        account_rows = conn.execute(select(account_table)).all()
        assert len(account_rows) == 1
        account = account_rows[0]
        assert account.id == 1
        assert account.user_id == 123
        assert account.created_at is not None
