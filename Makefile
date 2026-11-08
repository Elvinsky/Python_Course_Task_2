.DEFAULT_GOAL := check
.PHONY: setup env db-up db-down migrate seed run lint typecheck test check fmt

setup:            ## create the virtual environment (.venv) and install everything from uv.lock
	uv python install 3.14
	uv sync

env:              ## create your local .env from the example (does not overwrite)
	cp -n .env.example .env || true

db-up:            ## start PostgreSQL (Docker) and wait until it is healthy
	docker compose up -d --wait db

db-down:          ## stop PostgreSQL (data is kept in a Docker volume)
	docker compose down

migrate:          ## apply Alembic migrations to the database in DATABASE_URL
	uv run alembic upgrade head

seed:             ## load data/products.json into the database (AC 1)
	uv run python -m scripts.seed

run:              ## start the API with auto-reload: http://127.0.0.1:8000/docs
	uv run uvicorn app.main:app --reload

lint:             ## style and static checks
	uv run ruff check .
	uv run ruff format --check .

typecheck:        ## strict type checks
	uv run mypy .

test:             ## acceptance tests + your own tests (no Docker or network needed)
	uv run pytest

check: lint typecheck test   ## everything: this is the definition of "green"

fmt:              ## auto-fix what can be fixed
	uv run ruff check --fix .
	uv run ruff format .
