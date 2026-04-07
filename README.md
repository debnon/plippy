# plippy

Minimal Postgres + Python setup for persisting users.

## Run with Make

Start Postgres in the background:

```bash
make up
```

Run the Python example once (creates table and inserts a user):

```bash
make run
```

Stop services:

```bash
make down
```

If you want to remove database data too:

```bash
make clean
```

Useful checks:

```bash
make ps
make logs
```

## Run with Docker Compose

Start Postgres in the background:

```bash
docker compose up -d db
```

Run the Python example once (creates table and inserts a user):

```bash
docker compose run --rm app
```

Stop services:

```bash
docker compose down
```

If you want to remove database data too:

```bash
docker compose down -v
```