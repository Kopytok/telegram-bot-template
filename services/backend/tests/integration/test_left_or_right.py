import pytest

from fastapi.testclient import TestClient
from backend.api import app
from backend.repos.factory import get_bot_message_repo
from backend.repos.memory.bot_message import InMemoryBotMessageRepo

client = TestClient(app)


@pytest.mark.parametrize(
    "left,right,expected",
    (
        (True, True, "Left Yo Right"),
        (True, False, "Left Yo"),
        (False, True, "Yo Right"),
        (False, False, "Yo"),
    )
)
def test_left_or_right(left, right, expected):
    # Setup
    fake_bot_message_repo = InMemoryBotMessageRepo()
    fake_bot_message_repo.create(123, 9, "Yo")
    app.dependency_overrides[get_bot_message_repo] = \
        lambda: fake_bot_message_repo

    # Run
    res = client.post(
        "/left_or_right",
        json={"message_id": 123, "left": left, "right": right},
    )

    # Check
    assert res.status_code == 200, f"{res}"
    assert res.json()["text"] == expected
