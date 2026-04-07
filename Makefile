.PHONY: up run down clean logs ps

up:
	docker compose up -d db

run:
	docker compose run --rm app

down:
	docker compose down

clean:
	docker compose down -v

logs:
	docker compose logs -f db

ps:
	docker compose ps