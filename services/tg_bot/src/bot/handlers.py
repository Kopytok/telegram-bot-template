from aiogram import Router
from aiogram.types import Message
from aiohttp import ClientSession
from bot.keyboard import main_keyboard

router = Router()

BACKEND_URL = "http://backend:8000/message"


async def send_to_backend(user_id: int, text: str) -> str:
    async with ClientSession() as session:
        async with session.post(
            BACKEND_URL,
            json={"user_id": user_id, "text": text}
        ) as res:
            res.raise_for_status()
            data = await res.json()
            return data["reply"]


@router.message(lambda m: m.text)
async def any_text(message: Message):
    assert message.text is not None
    assert message.from_user is not None

    backend_reply = await send_to_backend(
        message.from_user.id,
        message.text,
    )
    await message.answer(backend_reply)


@router.message()
async def default(message: Message):
    await message.answer(
        "Choose:",
        reply_markup=main_keyboard(),
    )
