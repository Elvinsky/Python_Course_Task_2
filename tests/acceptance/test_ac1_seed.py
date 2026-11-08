"""AC 1: seed mock JSON product data into the database with an async seed script."""

import inspect
import json

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models import Item
from scripts import seed as seed_module
from scripts.seed import DATA_FILE, load_products, seed


async def _count(factory: async_sessionmaker[AsyncSession]) -> int:
    async with factory() as session:
        return (await session.scalar(select(func.count()).select_from(Item))) or 0


def test_mock_product_data_is_valid_json() -> None:
    products = json.loads(DATA_FILE.read_text())
    assert len(products) >= 12
    assert len({p["sku"] for p in products}) == len(products), (
        "skus in products.json must be unique"
    )
    assert all({"sku", "name", "price", "stock"} <= set(p) for p in products)


def test_seed_is_an_async_script_with_an_entry_point() -> None:
    assert inspect.iscoroutinefunction(seed), "seed() must be `async def`"
    source = inspect.getsource(seed_module)
    assert "asyncio.run" in source and '__name__ == "__main__"' in source, (
        "keep the `python -m scripts.seed` entry point"
    )


async def test_seed_inserts_every_product(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with session_factory() as session:
        inserted = await seed(session)

    assert inserted == len(load_products())
    # a different session must see the rows: seed() has to commit
    assert await _count(session_factory) == len(load_products()), (
        "rows are not visible to another session: commit!"
    )


async def test_seed_is_idempotent(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async with session_factory() as session:
        await seed(session)
    async with session_factory() as session:
        assert await seed(session) == 0, "a second run must insert nothing"
    assert await _count(session_factory) == len(load_products())


async def test_seed_only_inserts_missing_products(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    first = load_products()[0]
    async with session_factory() as session:
        session.add(Item(sku=first["sku"], name="Existing", price=1.0, stock=1))
        await session.commit()

    async with session_factory() as session:
        inserted = await seed(session)

    assert inserted == len(load_products()) - 1
    async with session_factory() as session:
        existing = await session.scalar(select(Item).where(Item.sku == first["sku"]))
    assert existing is not None and existing.name == "Existing", (
        "existing rows must not be overwritten"
    )
