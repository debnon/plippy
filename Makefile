.PHONY: up run api down clean logs ps build test test-integration

COMPOSE := $(shell docker compose version >/dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

up:
	$(COMPOSE) up -d db

build:
	$(COMPOSE) build app

run: build
	$(COMPOSE) run --rm app sh -c 'PYTHONPATH=/app/src python -m plippy.scripts.example'

api: build
	$(COMPOSE) run --rm --service-ports app sh -c 'PYTHONPATH=/app/src uvicorn plippy.api:app --host 0.0.0.0 --port 8000'

down:
	$(COMPOSE) down

clean:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f db

ps:
	$(COMPOSE) ps

test: build
	$(COMPOSE) run --rm app sh -c 'PYTHONPATH=/app/src pytest -q -m "not integration"'

test-integration: build
	$(COMPOSE) run --rm app sh -c 'PYTHONPATH=/app/src pytest -q -m integration'