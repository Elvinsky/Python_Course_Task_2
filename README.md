<!--
  Generated from the Python Kick-Start course: the description and acceptance criteria match the
  task window of the course app. Do not edit by hand; changes are made in the course repository.
-->

# Practical Task 2: Product Inventory Catalog API

> Part of **Python Kick-Start**: Section 2: “Touching the Grass” — Unauthenticated CRUD Server (5–7 Days). This repository is a **forkable starting point**:
> fork it, clone your fork, and build the task.

## 1. Set up your virtual environment first

> **Do this before you touch any code.** Every task in the course runs inside an isolated virtual
> environment, so dependencies never leak into your system Python (there is no `node_modules`-style
> implicit lookup in Python). Nothing in this repository is guaranteed to work outside it.

You need [git](https://git-scm.com/) and [uv](https://docs.astral.sh/uv/getting-started/installation/)
(a fast package and environment manager that also installs Python for you).

```bash
# install uv once: https://docs.astral.sh/uv/getting-started/installation/
uv python install 3.14
uv sync
uv run python --version

# then lint, type-check and test your work
make check
```

What these commands do:

- `uv python install 3.14` downloads Python 3.14 (the version pinned in `.python-version`). Python 3.12 is the
  minimum the acceptance criteria allow; use 3.13 only if a dependency has no wheels for 3.14 yet.
- `uv sync` creates the `.venv` folder and installs the locked dependencies into it.
- `uv run <command>` always runs inside that environment, so you do not have to activate it. If you prefer to
  activate it: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows).
- `uv run python --version` must print `Python 3.14.x` (or at least 3.12). If it prints another version, stop and fix
  the environment before continuing.

Common problems:

- `uv: command not found`: install uv and open a new terminal.
- Wrong Python version: run `uv python list` and `uv python install 3.14`, then delete `.venv` and run `uv sync` again.
- `make: command not found` (Windows): run the commands from the `Makefile` by hand, or use WSL / Git Bash.

## 2. Fork, clone and work on your fork

1. **Fork** [Python_Course_Task_2](https://github.com/Elvinsky/Python_Course_Task_2) to your own GitHub account (the *Fork* button, top right).
2. **Clone your fork** (not this repository):

   ```bash
   git clone https://github.com/<your-username>/Python_Course_Task_2.git
   cd Python_Course_Task_2
   ```

3. Set up the virtual environment (section 1), then create a branch: `git switch -c solution`.
4. Build the task step by step and commit small steps. Run `make check` before every push so you always know where you stand.

## 3. Task description

Build an unauthenticated REST API for a product inventory catalog on top of PostgreSQL. You will practice async FastAPI routing, Pydantic v2 validation, SQLAlchemy 2.0 async sessions, tuned connection pooling, Alembic migrations and async API tests, and end with a self-documenting API you can click through in Swagger UI. You start from a fork of the template repository that contains only the tooling (see below): you create the FastAPI application, the database model, the seed data, the Alembic setup and the tests yourself, and you provide your own PostgreSQL (for example with Docker Compose). Set up the virtual environment first, before you edit anything.

## 4. What already exists in this repository

- `.python-version`: pins Python 3.14 for uv
- `pyproject.toml` and `uv.lock`: the dependencies (FastAPI, Uvicorn, SQLAlchemy 2.0 async, asyncpg, Alembic, pydantic-settings; dev: pytest, pytest-asyncio, httpx, Ruff, Mypy) and the Ruff, Mypy (strict) and pytest configuration you wrote in Task 1
- `Makefile`: `make setup`, `make lint`, `make typecheck`, `make test`, `make check` and `make fmt`
- `.gitignore` for Python projects (`.venv`, caches, `.env`)

Everything else is yours to create: the application package, the database model, the seed data, the Alembic setup,
a way to run PostgreSQL, and the tests. Until you have written tests, `make test` fails because pytest finds none: that is expected.

## 5. What you need to do (acceptance criteria)

- [ ] **AC 1**: Run PostgreSQL locally (for example with Docker Compose), create an `Item` model (SQLAlchemy 2.0, async) with at least a unique `sku`, a `name`, a `price` and a `stock`, and load 10+ mock products from a JSON file you create with an async seed script that can run twice without duplicating rows.
- [ ] **AC 2**: Implement REST endpoints: `GET /items`, `GET /items/{id}`, `POST /items`, `PATCH /items/{id}`, `DELETE /items/{id}`, with Pydantic v2 schemas and sensible status codes (201, 204, 404, 409 for a duplicate `sku`, 422).
- [ ] **AC 3**: Set up SQLAlchemy `create_async_engine` with `pool_size=10` and `max_overflow=20`.
- [ ] **AC 4**: Verify interactive Swagger docs at `/docs`: all five operations are listed with their status codes.
- [ ] **AC 5**: Create the schema with an Alembic migration (`alembic upgrade head`), not `create_all`.
- [ ] **AC 6**: Write `pytest` tests for all five endpoints using `httpx.AsyncClient`, including 404 and 422 cases.

## 6. Tech stack requirements

- Python 3.12+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0 (async)
- asyncpg
- Alembic
- PostgreSQL
- Uvicorn
- pytest + httpx

## 7. Recommended stack

**Python version:** Python 3.14 (current stable). Fall back to 3.13 if asyncpg or another compiled dependency lacks wheels for 3.14; 3.12 is the minimum the ACs allow.

**API**

- FastAPI + Uvicorn (`uvicorn[standard]`): async framework and ASGI server; `--reload` for development
- Pydantic v2 + pydantic-settings: request/response schemas and typed configuration from environment variables

**Database**

- PostgreSQL 16+: run it with Docker Compose; use the official image
- SQLAlchemy 2.0 (async) + asyncpg: ORM and the fastest async PostgreSQL driver; engine pooling is configured in `app/database.py`
- Alembic (`alembic init -t async`): versioned schema migrations

**Testing & tooling**

- pytest + pytest-asyncio (`asyncio_mode = "auto"`) + httpx: async API tests with an in-process ASGI transport
- Ruff + Mypy (strict): carry over the Task 1 setup unchanged
- Docker Compose: one command for PostgreSQL (and later Redis)
- A DB client (psql, DBeaver or TablePlus): inspect the seeded data and the pool behaviour

**Avoid**

- psycopg2 or other sync drivers and `requests` inside `async def` handlers (they block the event loop)
- `Base.metadata.create_all` as your schema strategy (use Alembic)
- A module-level global session shared between requests
- Returning ORM objects without a `response_model`

## 8. Architecture guidelines

- Separate Pydantic schemas (request/response) from ORM models; never return ORM objects without a `response_model`.
- One async session per request, provided through a `Depends(get_db)` dependency.
- No blocking I/O inside `async def`: use async drivers, or declare the handler with plain `def` so FastAPI runs it in a threadpool.
- Return proper status codes: 201 on create, 204 on delete, 404 for unknown ids, 422 comes from Pydantic.
- Use `PATCH` with a schema of optional fields and `model_dump(exclude_unset=True)` for partial updates.
- Make the seed script idempotent and run it explicitly (for example `python -m scripts.seed`), never at app start-up.
- Pass the connection string through `pydantic-settings`; add `pool_recycle` if your DB closes idle connections.

## 9. Study first

Topics from the Python Kick-Start roadmap for this section:

- **Async Python: asyncio vs the JS Event Loop**: [asyncio documentation](https://docs.python.org/3/library/asyncio.html) · [FastAPI: concurrency and async / await](https://fastapi.tiangolo.com/async/) · [Glossary: global interpreter lock](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) · [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- **Pydantic v2 & Settings**: [Pydantic documentation](https://docs.pydantic.dev/latest/) · [Pydantic: settings management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **FastAPI & Async Routing**: [FastAPI tutorial: First steps](https://fastapi.tiangolo.com/tutorial/first-steps/) · [Pydantic documentation](https://docs.pydantic.dev/latest/)
- **Relational DB Connection Pooling & ORM**: [Database pooling in FastAPI (asifmuhammad.com)](https://asifmuhammad.com/articles/database-pooling-fastapi) · [SQLModel documentation](https://sqlmodel.tiangolo.com/) · [SQLAlchemy asyncio extension](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- **Schema Migrations with Alembic**: [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) · [Alembic: autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) · [Alembic cookbook: asyncio](https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic)
- **Testing Async APIs**: [FastAPI: async tests](https://fastapi.tiangolo.com/advanced/async-tests/) · [FastAPI: testing dependencies with overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) · [HTTPX: async support](https://www.python-httpx.org/async/)

## Definition of done

- [ ] every acceptance criterion above is met
- [ ] `make check` is green
- [ ] your Alembic migration, `uv.lock` and the seed data are committed; `.env` files and `.venv` are not
