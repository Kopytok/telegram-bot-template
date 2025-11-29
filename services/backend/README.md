# Backend logic of the bot

The container is used to implement bot business logic

## Prerequisites

Place your `DATABASE_URL` in the `.env` file within this directory, e.g.:

```bash
# services/backend/.env
DATABASE_URL=postgresql+psycopg2://app_user:app_password@db:5432/app_db
```

## Current logic

Incoming messages are stored in the database. The bot responds with tripled text of the received message.

TODO:
- add Users table to store user info
- add Counter of characters in all received from user messages, as example of business logic
