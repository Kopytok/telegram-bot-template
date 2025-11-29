# Telegram API interface

Container is used to:
1. receive messages from Telegram API
2. forward requests to other containers
3. send messages back to Telegram users

Place your bot token in the `.env` file within this directory, e.g.:

```bash
# services/tg_bot/.env
BOT_TOKEN=888888888:GGGGGGGGGG-jjjjjjjjjjjjjjjjj-III-ll
```

## Available functions

Currently, all messages are forwarded to backend `/message` endpoint. After backend responses, the answer is sent back to the user.
