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
def test_some_endpoint(left, right, expected):
    res = client.post(
        "/some_endpoint",
        json={"message_id": 123, "left": left, "right": right},
    )
    assert res.status_code == 200, f"{res}"
    assert res.json()["text"] == expected
