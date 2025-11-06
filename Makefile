dev:
	uv run flask --app travel_app.app run --debug --port 8000

migrate:
	docker run --rm \
		-v "./migrations:/flyway/sql" \
		--env-file .env \
		flyway/flyway migrate
