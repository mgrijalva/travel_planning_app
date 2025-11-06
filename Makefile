dev:
	uv run flask --app travel_app.app run --debug --port 8000

migrate:
	docker run --rm \
		-v "./migrations:/flyway/sql" \
		--env-file .env \
		flyway/flyway migrate

test:
	uv run pytest travel_app

format.check:
	uv run black --check travel_app

format:
	uv run black travel_app

lint:
	uv run flake8 travel_app

typecheck:
	uv run pyright
