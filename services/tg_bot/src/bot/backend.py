from aiohttp import ClientSession
from bot.const import BACKEND_URL


async def send_left_or_right(
    message_id: int,
    left: bool,
    right: bool,
) -> str:
    payload = {
        "message_id": message_id,
        "left": left,
        "right": right,
    }

    async with ClientSession() as session:
        async with session.post(
            BACKEND_URL+"/left_or_right",
            json=payload,
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["text"]


async def save_answer_endpoint(
    message_id: int,
    chat_id: int,
    text: str,
) -> str:
    payload = {
        "message_id": message_id,
        "chat_id": chat_id,
        "text": text,
    }

    async with ClientSession() as session:
        async with session.post(
            BACKEND_URL+"/save_answer",
            json=payload,
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["status"]
