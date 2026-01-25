import pytest

from aiogram.types import InlineKeyboardMarkup

from bot.handlers import send_to_backend, handle_backend_reply
from fakes import FakeMessage, FakeClientSession


@pytest.mark.asyncio
async def test_send_to_backend_response(mocker):
    # Setup
    response_data = {"reply": "Backend response"}
    fake_session = FakeClientSession(response_data)
    mocker.patch(
        "bot.backend.ClientSession",
        return_value=fake_session,
    )

    # Run
    reply = await send_to_backend(123, "Hello")

    # Check
    assert reply == response_data
    post_call = fake_session.calls[0]
    assert post_call.url == "http://backend:8000/message"
    assert post_call.json == {"chat_id": 123, "text": "Hello"}


@pytest.mark.asyncio
async def test_fallback_shows_keyboard():
    # Setup
    message = FakeMessage.create(
        message_id=132,
        user_id=321,
        text="Random text",
    )
    backend_reply = {"reply": "Choose:", "keyboard_type": "main"}

    # Run
    await handle_backend_reply(message, backend_reply)

    # Check
    call = message.calls[0]
    assert call.reply_text == "Choose:"
    assert "reply_markup" in call.kwargs
    assert isinstance(call.kwargs["reply_markup"], InlineKeyboardMarkup)


@pytest.mark.asyncio
async def test_fallback_inline_flow():
    # Setup
    message = FakeMessage.create(
        message_id=132,
        user_id=321,
        text="Random text",
    )
    backend_reply = {
        "reply": "Choose:",
        "keyboard_type": "inline_flow",
    }

    # Run
    await handle_backend_reply(message, backend_reply)

    # Check
    assert len(message.calls) == 1

    first_call = message.calls[0]
    assert first_call.reply_text == "Choose:"
    assert "reply_markup" in first_call.kwargs
    assert isinstance(
        first_call.kwargs["reply_markup"],
        InlineKeyboardMarkup,
    ), "Should send Inline keyboard"
