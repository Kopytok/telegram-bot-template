from dataclasses import dataclass


@dataclass
class FakeClientSessionCall:
    url: str
    json: dict


class FakeResponse:

    def __init__(self, response_data: dict):
        self.response_data = response_data or {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        _ = exc_type, exc, tb

    def raise_for_status(self):
        pass

    async def json(self):
        return self.response_data


class FakeClientSession:

    def __init__(self, response_data: dict):
        self.response_data = response_data
        self.calls = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        _ = exc_type, exc, tb

    def post(self, url: str, json: dict):
        self.calls.append(FakeClientSessionCall(url, json))
        return FakeResponse(self.response_data)
