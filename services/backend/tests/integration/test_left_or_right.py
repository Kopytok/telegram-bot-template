import pytest

from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)


@pytest.mark.parametrize(
    "left,right,expected",
    (
        (True, True, "Left YO Right"),
        (True, False, "Left YO"),
        (False, True, "YO Right"),
        (False, False, "YO"),
    )
)
def test_left_or_right(mocker, left, right, expected):
    # Setup
    mocker.patch("backend.api.get_bot_message_text", return_value="YO")

    # Run
    res = client.post(
        "/left_or_right",
        json={"message_id": 123, "left": left, "right": right},
    )

    # Check
    assert res.status_code == 200, f"{res}"
    assert res.json()["text"] == expected
