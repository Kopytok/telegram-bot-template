from aiohttp import ClientSession
from bot.settings import BACKEND_URL


async def send_some_endpoint(
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
            BACKEND_URL+"/some_endpoint",
            json=payload,
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["text"]


async def save_answer_endpoint(
    message_id: int,
    user_id: int,
    text: str,
) -> str:
    payload = {
        "message_id": message_id,
        "user_id": user_id,
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
