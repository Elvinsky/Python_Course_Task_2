"""AC 3: SQLAlchemy `create_async_engine` is configured with pool_size=10 and max_overflow=20."""

from typing import Any, cast

from sqlalchemy.pool import QueuePool

from app.database import engine

POOL = cast("Any", engine.pool)


def test_engine_uses_a_queue_pool() -> None:
    assert isinstance(engine.pool, QueuePool), f"expected a QueuePool, got {type(engine.pool)}"


def test_pool_size_is_10() -> None:
    assert POOL.size() == 10, "pass pool_size=10 to create_async_engine in app/database.py"


def test_max_overflow_is_20() -> None:
    assert POOL._max_overflow == 20, (
        "pass max_overflow=20 to create_async_engine in app/database.py"
    )
