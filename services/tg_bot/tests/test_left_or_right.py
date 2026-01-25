import pytest

from bot.backend import send_left_or_right
from fakes import FakeClientSession


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "left,right,expected", (
        (True, False, "Left YO"),
        (False, True, "YO Right"),
    )
)
async def test_send_left_or_right(
    mocker,
    left,
    right,
    expected,
):
    # Setup
    response_data = {"text": expected}
    fake_session = FakeClientSession(response_data)
    mocker.patch(
        "bot.backend.ClientSession",
        return_value=fake_session,
    )

    # Run
    received = await send_left_or_right(123, left, right)

    # Check
    assert received == expected
    post_call = fake_session.calls[0]
    assert post_call.url == "http://backend:8000/left_or_right"
    assert post_call.json == {"message_id": 123, "left": left, "right": right}
