import pytest

from fastapi.testclient import TestClient
from backend.api import app
from backend.repos.factory import (
    get_bot_message_repo,
    get_answer_config_repo,
)
from backend.repos.memory.bot_message import InMemoryBotMessageRepo
from backend.repos.memory.answer_config import InMemoryAnswerConfigRepo

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
def test_left_right_switch_from_false(left, right, expected):
    # Setup
    fake_bot_message_repo = InMemoryBotMessageRepo()
    fake_bot_message_repo.create(123, 9, "Yo")
    app.dependency_overrides[get_bot_message_repo] = \
        lambda: fake_bot_message_repo

    fake_answer_config_repo = InMemoryAnswerConfigRepo()
    app.dependency_overrides[get_answer_config_repo] = \
        lambda: fake_answer_config_repo

    # Run
    res = client.post(
        "/left_right_switch",
        json={
            "message_id": 123,
            "chat_id": 8,
            "toggle_left": left,
            "toggle_right": right,
        },
    )

    # Check
    assert res.status_code == 200, f"{res}"
    assert res.json()["text"] == expected


@pytest.mark.parametrize(
    "left,right,expected",
    (
        (True, True, "Yo"),
        (True, False, "Yo Right"),
        (False, True, "Left Yo"),
        (False, False, "Left Yo Right"),
    )
)
def test_left_right_switch_from_true(left, right, expected):
    # Setup
    chat_id = 9
    fake_bot_message_repo = InMemoryBotMessageRepo()
    fake_bot_message_repo.create(123, chat_id, "Yo")
    app.dependency_overrides[get_bot_message_repo] = \
        lambda: fake_bot_message_repo

    fake_answer_config_repo = InMemoryAnswerConfigRepo()
    fake_answer_config_repo.set_config(chat_id, True, True)
    app.dependency_overrides[get_answer_config_repo] = \
        lambda: fake_answer_config_repo

    # Run
    res = client.post(
        "/left_right_switch",
        json={
            "message_id": 123,
            "chat_id": chat_id,
            "toggle_left": left,
            "toggle_right": right,
        },
    )

    # Check
    assert res.status_code == 200, f"{res}"
    assert res.json()["text"] == expected
