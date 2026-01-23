import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "EMPTY")

if BOT_TOKEN == "EMPTY":
    raise RuntimeError("BOT_TOKEN is not set! Put it in .env")

BACKEND_URL = "http://backend:8000"
