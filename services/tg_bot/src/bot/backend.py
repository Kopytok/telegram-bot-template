from aiohttp import ClientSession
from bot.settings import BACKEND_URL


async def send_some_endpoint(
    action: str,
    text: str,
) -> str:
    payload = {
        "action": action,
        "text": text,
    }

    async with ClientSession() as session:
        async with session.post(
            BACKEND_URL+"/some_endpoint",
            json=payload,
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["text"]
