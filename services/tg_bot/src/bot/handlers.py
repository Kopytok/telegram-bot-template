from typing import Optional
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiohttp import ClientSession
from bot.keyboard import (
    inline_keyboard,
    left_right_keyboard,
)
from bot.backend import (
    send_some_endpoint,
    save_answer_endpoint,
)
from bot.const import BACKEND_URL

router = Router()


async def send_to_backend(
    chat_id: int,
    text: str,
) -> dict:
    payload = {"chat_id": chat_id, "text": text}

    async with ClientSession() as session:
        async with session.post(BACKEND_URL+"/message", json=payload) as res:
            res.raise_for_status()
            return await res.json()


@router.message()
async def any_text(message: Message) -> None:
    """
    Main handler. Recognizes buttons, forwards any text message
    to the backend and replies with the backend's response
    """
    request_text: str = message.text or ""

    backend_reply = await send_to_backend(
        chat_id=message.chat.id,
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
        kb = left_right_keyboard()

    response = await message.answer(
        reply_text,
        reply_markup=kb,
    )
    await save_answer_endpoint(
        message_id=response.message_id,
        chat_id=response.chat.id,
        text=reply_text,
    )


@router.callback_query(F.data.in_(["LEFT", "RIGHT"]))
async def on_left_right_callback(query: CallbackQuery) -> None:
    await query.answer()

    message = query.message
    if message is None:
        return

    message_id = message.message_id
    left = True if query.data == "LEFT" else False
    right = True if query.data == "RIGHT" else False

    new_text = await send_some_endpoint(message_id, left, right)

    await message.edit_text(
        new_text,
        reply_markup=left_right_keyboard(),
    )
