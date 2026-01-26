from fastapi.testclient import TestClient

from backend.api import app
from backend.repos.factory import (
    get_user_message_repo,
    get_account_repo,
)
from backend.repos.memory.account import InMemoryAccountRepo
from backend.repos.memory.user_message import InMemoryUserMessageRepo

client = TestClient(app)


def test_message_endpoint_persists_message():
    # Setup
    fake_user_message_repo = InMemoryUserMessageRepo()
    app.dependency_overrides[get_user_message_repo] = \
        lambda: fake_user_message_repo
    fake_account_repo = InMemoryAccountRepo()
    app.dependency_overrides[get_account_repo] = \
        lambda: fake_account_repo
    chat_id = 123

    # Run
    resp = client.post(
        "/message",
        json={"chat_id": chat_id, "text": "Hello"},
    )

    # Check
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"reply": "Hello Hello Hello", "keyboard_type": None}

    assert fake_account_repo.exists(chat_id)
    [received_text] = fake_user_message_repo.get_texts(chat_id)
    assert received_text == "Hello"
