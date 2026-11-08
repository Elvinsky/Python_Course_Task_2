.DEFAULT_GOAL := check
.PHONY: setup lint typecheck test check fmt

setup:
	uv python install 3.14
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run mypy .

test:
	uv run pytest

check: lint typecheck test

fmt:
	uv run ruff check --fix .
	uv run ruff format .
