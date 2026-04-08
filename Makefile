.PHONY: up run down clean logs ps build test test-integration

COMPOSE := $(shell docker compose version >/dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

up:
	$(COMPOSE) up -d db

build:
	$(COMPOSE) build app

run: build
	$(COMPOSE) run --rm app

down:
	$(COMPOSE) down

clean:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f db

ps:
	$(COMPOSE) ps

test: build
	$(COMPOSE) run --rm app sh -c 'PYTHONPATH=/app pytest -q -m "not integration"'

test-integration: build
	$(COMPOSE) run --rm app sh -c 'PYTHONPATH=/app pytest -q -m integration'