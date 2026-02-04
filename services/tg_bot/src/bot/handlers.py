from typing import Optional
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.keyboard import (
    inline_keyboard,
    left_right_keyboard,
)
from bot.backend import (
    send_to_backend,
    send_left_right_switch,
    save_answer_endpoint,
)

router = Router()


async def handle_backend_reply(
    message: Message,
    backend_reply: dict,
) -> Message:
    reply_text: str = backend_reply["reply"]
    keyboard_type: Optional[str] = backend_reply.get("keyboard_type")

    if keyboard_type == "inline_flow":
        kb = inline_keyboard()
    else:
        kb = left_right_keyboard()

    return await message.answer(
        reply_text,
        reply_markup=kb,
    )


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

    response = await handle_backend_reply(
        message=message,
        backend_reply=backend_reply,
    )

    await save_answer_endpoint(
        message_id=response.message_id,
        chat_id=response.chat.id,
        text=backend_reply["reply"],
    )


@router.callback_query(F.data.in_(["LEFT", "RIGHT"]))
async def on_left_right_switch_callback(query: CallbackQuery) -> None:
    await query.answer()

    message = query.message
    if message is None:
        return

    message_id = message.message_id
    chat_id = message.chat.id
    left = True if query.data == "LEFT" else False
    right = True if query.data == "RIGHT" else False

    new_text = await send_left_right_switch(message_id, chat_id, left, right)

    await message.edit_text(
        new_text,
        reply_markup=left_right_keyboard(),
    )
