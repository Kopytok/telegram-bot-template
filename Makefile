build:
	docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down -v

psql:
	docker compose exec db psql -U app_user -d app_db
