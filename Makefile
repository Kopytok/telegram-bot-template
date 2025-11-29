build:
	docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down -v

psql:
	docker compose exec db psql -U app_user -d app_db

restart-bot:
	docker compose restart tg_bot

restart-backend:
	docker compose restart backend
