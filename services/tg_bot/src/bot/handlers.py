from typing import Optional
from aiogram import Router
from aiogram.types import Message
from aiohttp import ClientSession
from bot.keyboard import (
    inline_keyboard,
)

router = Router()

BACKEND_URL = "http://backend:8000/message"


async def send_to_backend(
    user_id: int,
    text: str,
) -> dict:
    payload = {"user_id": user_id, "text": text}

    async with ClientSession() as session:
        async with session.post(BACKEND_URL, json=payload) as res:
            res.raise_for_status()
            return await res.json()


@router.message()
async def any_text(message: Message) -> None:
    """
    Main handler. Recognizes buttons, forwards any text message
    to the backend and replies with the backend's response
    """
    try:
        assert message.from_user is not None
    except AssertionError:
        # This should never happen
        return

    request_text: str = message.text or ""

    backend_reply = await send_to_backend(
        user_id=message.from_user.id,
        text=request_text,
    )

    await handle_backend_reply(message, backend_reply)


async def handle_backend_reply(
    message: Message,
    backend_reply: dict,
) -> None:
    reply_text: str = backend_reply["reply"]
    keyboard_type: Optional[str] = backend_reply.get("keyboard_type")

    if keyboard_type == "inline_flow":
        kb = inline_keyboard()
    else:
        kb = None

    await message.answer(
        reply_text,
        reply_markup=kb,
    )
