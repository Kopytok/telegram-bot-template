import pytest

from bot.backend import send_left_right_switch
from fakes import FakeClientSession


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "left,right,expected", (
        (True, False, "Left YO"),
        (False, True, "YO Right"),
    )
)
async def test_send_left_right_switch(
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
    received = await send_left_right_switch(123, 1, left, right)

    # Check
    assert received == expected
    post_call = fake_session.calls[0]
    assert post_call.url == "http://backend:8000/left_right_switch"
    assert post_call.json == {
        "message_id": 123,
        "chat_id": 1,
        "toggle_left": left,
        "toggle_right": right,
    }
