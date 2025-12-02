import pytest
from bot.handlers import send_to_backend, handle_backend_reply
from fakes import FakeMessage


@pytest.mark.asyncio
async def test_send_to_backend_response(mocker):
    # Setup
    response = mocker.AsyncMock()
    response.json = mocker.AsyncMock(
        return_value={"reply": "Backend response"}
    )
    response.raise_for_status = mocker.Mock()

    post_cm = mocker.AsyncMock()
    post_cm.__aenter__.return_value = response
    post_cm.__aexit__.return_value = None

    session = mocker.Mock()
    session.__aenter__ = mocker.AsyncMock(return_value=session)
    session.__aexit__ = mocker.AsyncMock(return_value=None)

    session.post = mocker.Mock(return_value=post_cm)

    mocker.patch("bot.handlers.ClientSession", return_value=session)

    # Run
    reply = await send_to_backend(123, "Hello")

    # Check
    assert reply == {"reply": "Backend response"}
    session.post.assert_called_once_with(
        "http://backend:8000/message",
        json={"user_id": 123, "text": "Hello"}
    )


@pytest.mark.asyncio
async def test_fallback_shows_keyboard():
    # Setup
    message = FakeMessage.create(user_id=321, text="Random text")
    backend_reply = {"reply": "Choose:", "keyboard_type": "main"}

    # Run
    await handle_backend_reply(message, backend_reply)

    # Check
    call = message.calls[-1]
    assert call.reply_text == "Choose:"
    assert "reply_markup" in call.kwargs
