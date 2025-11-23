local_setup:
	uv sync && uv pip install -e .

build:
	docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down -v

test:
	pytest
