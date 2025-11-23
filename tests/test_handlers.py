import pytest
from aiogram import types
from bot.handlers import press_a, press_b, default


@pytest.mark.asyncio
async def test_press_a(mocker):
    # Setup
    message = mocker.Mock(spec=types.Message)
    message.text = "A"
    message.answer = mocker.AsyncMock()

    # Run
    await press_a(message)

    # Check
    message.answer.assert_called_once_with("You pressed A")


@pytest.mark.asyncio
async def test_press_b(mocker):
    # Setup
    message = mocker.Mock(spec=types.Message)
    message.text = "B"
    message.answer = mocker.AsyncMock()

    # Run
    await press_b(message)

    # Check
    message.answer.assert_called_once_with("You pressed B")


@pytest.mark.asyncio
async def test_fallback_shows_keyboard(mocker):
    # Setup
    message = mocker.Mock(spec=types.Message)
    message.text = "Something else"
    message.answer = mocker.AsyncMock()

    # Run
    await default(message)

    # Check
    # Expect call with text + ANY keyboard markup
    # We only test the first argument (text)
    message.answer.assert_called()
    args, kwargs = message.answer.call_args

    assert args[0] == "Choose:"
    assert "reply_markup" in kwargs
