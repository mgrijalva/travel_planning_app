# Travel Planner app

## Setup

1. Install uv: https://github.com/astral-sh/uv?tab=readme-ov-file#installation
2. Run `cp .env.example .env`
3. Setup your database by running `make migrate`
4. Run `make dev` to start the server

## Database Migrations

1. Create a sql file under `migrations/` following the naming convention. e.g. `V24__add_new_table.sql`
2. Apply the migration with `make migrate`
