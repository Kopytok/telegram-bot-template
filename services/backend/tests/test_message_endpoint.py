import pytest
from httpx import AsyncClient

from backend.main import app


@pytest.mark.asyncio
async def test_message_endpoint():
    # Trigger
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post(
            "/message",
            json={"user_id": 123, "text": "Hello"},
        )

    # Check
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"reply": "Hello Hello Hello"}
