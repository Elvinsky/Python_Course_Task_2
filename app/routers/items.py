"""CRUD endpoints for /items."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Item
from app.schemas import ItemCreate, ItemOut, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemOut])
async def list_items(db: AsyncSession = Depends(get_db)) -> Sequence[Item]:
    """Worked example (provided): list every item ordered by id."""
    result = await db.scalars(select(Item).order_by(Item.id))
    return result.all()


# TODO (AC 2): implement the four handlers below. The contract the acceptance tests check:
#   GET    /items/{item_id}  -> 200 + item                         | 404 if unknown
#   POST   /items            -> 201 + created item                 | 409 duplicate sku, 422 invalid
#   PATCH  /items/{item_id}  -> 200 + updated item (partial)       | 404 if unknown, 422 invalid
#   DELETE /items/{item_id}  -> 204 without a body                 | 404 if unknown
# TODO (AC 4): make the generated Swagger docs say so: set `status_code=` on POST and DELETE,
# and document the error cases with `responses={404: {"description": "Item not found"}}`
# (and 409 for POST). Write the dict inline in the decorator: if you share it in a variable, mypy
# needs the annotation `dict[int | str, dict[str, Any]]`.
# Hints: `await db.get(Item, item_id)`, `payload.model_dump(exclude_unset=True)` for PATCH,
# `await db.commit()` after every write, and `IntegrityError` for a duplicate sku.


@router.get("/{item_id}", response_model=ItemOut)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)) -> Item:
    raise HTTPException(status_code=501, detail="TODO (AC 2): implement GET /items/{item_id}")


@router.post("", response_model=ItemOut)
async def create_item(payload: ItemCreate, db: AsyncSession = Depends(get_db)) -> Item:
    raise HTTPException(status_code=501, detail="TODO (AC 2): implement POST /items")


@router.patch("/{item_id}", response_model=ItemOut)
async def update_item(
    item_id: int, payload: ItemUpdate, db: AsyncSession = Depends(get_db)
) -> Item:
    raise HTTPException(status_code=501, detail="TODO (AC 2): implement PATCH /items/{item_id}")


@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)) -> None:
    raise HTTPException(status_code=501, detail="TODO (AC 2): implement DELETE /items/{item_id}")
