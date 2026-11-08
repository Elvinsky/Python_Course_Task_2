<!--
  Generated from the Python Kick-Start course: the description and acceptance criteria match the
  task window of the course app. Do not edit by hand; changes are made in the course repository.
-->

# Practical Task 2: Product Inventory Catalog API

> Part of **Python Kick-Start**: Section 2: “Touching the Grass” — Unauthenticated CRUD Server (5–7 Days). This repository is a **forkable template**:
> fork it, clone your fork, and implement everything marked `TODO` until all acceptance tests pass.

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

# then run every acceptance check (they fail until you finish the task)
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
4. Search for `TODO` to find everything you have to implement: `grep -rn "TODO" . --exclude-dir=.venv --exclude-dir=.git --exclude=README.md`.
5. Commit small steps and run `make check` before every push, so you always know which criteria are done.
6. Keep the acceptance tests in `tests/acceptance/` unchanged: they are the definition of "done" for each
   acceptance criterion. Write your own tests next to them.

## 3. Task description

Build an unauthenticated REST API for a product inventory catalog on top of PostgreSQL. You will practice async FastAPI routing, Pydantic v2 validation, SQLAlchemy 2.0 async sessions, tuned connection pooling, Alembic migrations and async API tests, and end with a self-documenting API you can click through in Swagger UI. You work in a fork of the template repository: the project configuration, models, Alembic setup, test fixtures and acceptance tests are provided, and the endpoints, schemas, seed script, migration and your own tests are marked `TODO`. Set up the virtual environment first, before you edit anything.

## 4. Acceptance criteria

- [ ] **AC 1**: Seed mock JSON product data into PostgreSQL using an async seed script.
- [ ] **AC 2**: Implement REST endpoints: `GET /items`, `GET /items/{id}`, `POST /items`, `PATCH /items/{id}`, `DELETE /items/{id}`.
- [ ] **AC 3**: Set up SQLAlchemy `create_async_engine` with `pool_size=10` and `max_overflow=20`.
- [ ] **AC 4**: Verify interactive Swagger docs at `/docs`.
- [ ] **AC 5**: Create the schema with an Alembic migration (`alembic upgrade head`), not `create_all`.
- [ ] **AC 6**: Write `pytest` tests for all five endpoints using `httpx.AsyncClient`, including 404 and 422 cases.

## 5. What the template gives you, and what is yours

The tooling from Task 1 (Ruff, Mypy `strict`, pytest, `Makefile`) is already configured, and `uv.lock` is committed
so everyone installs the same versions.

| Path | State | Purpose |
|---|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version`, `Makefile` | provided | dependencies and tool configuration, `make` shortcuts |
| `compose.yaml`, `.env.example` | provided | local PostgreSQL 16 (`db` service) and the settings to connect to it |
| `app/config.py` | provided | typed settings with `pydantic-settings` (`DATABASE_URL`, `ECHO_SQL`) |
| `app/models.py` | provided | SQLAlchemy 2.0 model `Item` (`id`, `sku` unique, `name`, `description`, `price`, `stock`) |
| `app/main.py` | provided | the FastAPI app; includes the items router |
| `app/database.py` | **TODO (AC 3)** | the engine exists without pooling options: configure the pool |
| `app/schemas.py` | **TODO (AC 2)** | `ItemOut` is provided; write `ItemCreate` and `ItemUpdate` with validation |
| `app/routers/items.py` | **TODO (AC 2, AC 4)** | `GET /items` is a worked example; implement the other four endpoints (they return `501` now) and document status codes |
| `scripts/seed.py` | **TODO (AC 1)** | implement `seed(session)`; `load_products()` and the `python -m scripts.seed` entry point are provided |
| `data/products.json` | provided | 14 mock products to seed |
| `alembic.ini`, `alembic/env.py` | provided | async Alembic setup (reads `DATABASE_URL`) |
| `alembic/versions/` | **TODO (AC 5)** | empty: generate the first migration |
| `tests/conftest.py` | provided | fixtures: temporary SQLite database, `session_factory`, and `client` (an `httpx.AsyncClient` talking to the app in-process) |
| `tests/test_items.py` | **TODO (AC 6)** | your own tests; one example is provided |
| `tests/acceptance/` | provided, do not edit | one file per acceptance criterion |

### How the acceptance tests map to the criteria

| Criterion | Checked by |
|---|---|
| AC 1 | `tests/acceptance/test_ac1_seed.py`: valid data file, `seed()` is `async`, inserts every product, commits, is idempotent, does not overwrite existing rows |
| AC 2 | `tests/acceptance/test_ac2_endpoints.py`: all five endpoints, status codes (`200`, `201`, `204`, `404`, `409`, `422`), validation, partial `PATCH`, ordering |
| AC 3 | `tests/acceptance/test_ac3_pool.py`: a `QueuePool` with `pool_size == 10` and `max_overflow == 20` |
| AC 4 | `tests/acceptance/test_ac4_swagger.py`: `/docs` and `/openapi.json` are served, all five operations are documented with request bodies and the right status codes (`201`, `204`, `404`, `409`) |
| AC 5 | `tests/acceptance/test_ac5_migrations.py`: a revision exists, `alembic upgrade head` creates `items` with a unique `sku`, `downgrade` removes it, no `create_all` under `app/` or `scripts/` |
| AC 6 | `tests/acceptance/test_ac6_own_tests.py`: your `tests/test_items.py` has at least 8 tests, calls `get`, `post`, `patch` and `delete` on the client, and expects `404` and `422` |

The tests need **no Docker and no network**: every test gets its own temporary SQLite database. Run everything with
`make check`. At the start it fails on purpose; it is green when you are done.

### The API contract

| Endpoint | Success | Errors |
|---|---|---|
| `GET /items` | `200` list ordered by `id` (provided) | |
| `GET /items/{item_id}` | `200` item | `404` unknown id |
| `POST /items` | `201` created item (`stock` defaults to `0`) | `409` duplicate `sku`, `422` invalid body |
| `PATCH /items/{item_id}` | `200` updated item; only the fields in the body change | `404` unknown id, `422` invalid body |
| `DELETE /items/{item_id}` | `204` with no body | `404` unknown id |

Validation: `sku` and `name` are not empty, `price >= 0`, `stock >= 0` (integers). The `sku` cannot be changed with `PATCH`.

## 6. Run the API locally

You need Docker for the real PostgreSQL database (the tests do not).

```bash
cp .env.example .env     # connection settings (git-ignored)
make db-up               # start PostgreSQL 16 and wait until it is healthy
make migrate             # alembic upgrade head (after you generated the first migration)
make seed                # python -m scripts.seed
make run                 # uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> for the interactive Swagger UI (and `/redoc` for ReDoc). Stop the database with
`make db-down`.

Generate the first migration once your model is final (AC 5), against the running database:

```bash
uv run alembic revision --autogenerate -m "create items"
```

Open the generated file in `alembic/versions/` and **read it** before applying it: autogenerate is a draft, not an oracle.

## 7. Connection pooling in two minutes

Opening a database connection is slow, so SQLAlchemy keeps a **pool** of them and lends one to each request.

- `pool_size=10`: up to 10 connections are kept open and reused.
- `max_overflow=20`: under a burst, up to 20 *extra* temporary connections may be opened (30 in total); they are closed
  again when returned. Request number 31 waits (`pool_timeout`, 30 s by default) and then fails.
- `pool_recycle=1800` (optional): replace connections older than 30 minutes, because firewalls and databases drop idle
  connections.
- `pool_pre_ping=True` (optional): test a connection before lending it, so a dropped connection does not fail a request.

The `get_db` dependency opens one `AsyncSession` per request; leaving `async with` returns its connection to the pool.
Keep the sum `(pool_size + max_overflow) x number of app processes` below PostgreSQL's `max_connections`.

## 8. Tech stack requirements

- Python 3.12+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0 (async)
- asyncpg
- Alembic
- PostgreSQL
- Uvicorn
- pytest + httpx

## 9. Recommended stack

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

## 10. Architecture guidelines

- Separate Pydantic schemas (request/response) from ORM models; never return ORM objects without a `response_model`.
- One async session per request, provided through a `Depends(get_db)` dependency.
- No blocking I/O inside `async def`: use async drivers, or declare the handler with plain `def` so FastAPI runs it in a threadpool.
- Return proper status codes: 201 on create, 204 on delete, 404 for unknown ids, 422 comes from Pydantic.
- Use `PATCH` with a schema of optional fields and `model_dump(exclude_unset=True)` for partial updates.
- Seed script is idempotent and run via `python -m scripts.seed`, not at app start-up.
- Pass the connection string through `pydantic-settings`; add `pool_recycle` if your DB closes idle connections.

## 11. Study first

Topics from the Python Kick-Start roadmap for this section:

- **Async Python: asyncio vs the JS Event Loop**: [asyncio documentation](https://docs.python.org/3/library/asyncio.html) · [FastAPI: concurrency and async / await](https://fastapi.tiangolo.com/async/) · [Glossary: global interpreter lock](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) · [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- **Pydantic v2 & Settings**: [Pydantic documentation](https://docs.pydantic.dev/latest/) · [Pydantic: settings management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **FastAPI & Async Routing**: [FastAPI tutorial: First steps](https://fastapi.tiangolo.com/tutorial/first-steps/) · [Pydantic documentation](https://docs.pydantic.dev/latest/)
- **Relational DB Connection Pooling & ORM**: [Database pooling in FastAPI (asifmuhammad.com)](https://asifmuhammad.com/articles/database-pooling-fastapi) · [SQLModel documentation](https://sqlmodel.tiangolo.com/) · [SQLAlchemy asyncio extension](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- **Schema Migrations with Alembic**: [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) · [Alembic: autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) · [Alembic cookbook: asyncio](https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic)
- **Testing Async APIs**: [FastAPI: async tests](https://fastapi.tiangolo.com/advanced/async-tests/) · [FastAPI: testing dependencies with overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) · [HTTPX: async support](https://www.python-httpx.org/async/)

## Definition of done

- [ ] `make check` is green
- [ ] `make migrate && make seed && make run` works against PostgreSQL, and every endpoint can be tried in `/docs`
- [ ] Your migration is committed under `alembic/versions/`
- [ ] Stretch: add pagination (`limit` / `offset`) and a `?q=` name filter to `GET /items`, with tests
