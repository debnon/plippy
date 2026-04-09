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

Run the API server:

```bash
make api
```

Then hit endpoints:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/users
curl -X POST http://localhost:8000/users \
	-H "Content-Type: application/json" \
	-d '{"name":"ben","funds":"25.50"}'
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

## Testing

Run fast tests (unit + sqlite model test):

```bash
make test
```

Run Postgres integration tests:

```bash
make test-integration
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