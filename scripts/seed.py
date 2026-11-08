"""Seed the database with the mock products in data/products.json (AC 1).

Run it against the database in DATABASE_URL (after `make migrate`):

    uv run python -m scripts.seed     # or: make seed
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session, engine

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "products.json"


def load_products(path: Path = DATA_FILE) -> list[dict[str, Any]]:
    """Provided: read the mock product data."""
    products: list[dict[str, Any]] = json.loads(path.read_text())
    return products


async def seed(session: AsyncSession) -> int:
    """Insert the products from `load_products()` and return how many rows were inserted.

    TODO (AC 1): implement it so that
      * every product in data/products.json ends up in the `items` table,
      * it is idempotent: products whose `sku` already exist are skipped, so a second run
        returns 0,
      * the work is committed (`await session.commit()`), because the caller does not do it.
    """
    raise NotImplementedError("TODO (AC 1): implement seed()")


async def main() -> None:
    async with async_session() as session:
        inserted = await seed(session)
    await engine.dispose()
    print(f"Seeded {inserted} new product(s).")


if __name__ == "__main__":
    asyncio.run(main())
