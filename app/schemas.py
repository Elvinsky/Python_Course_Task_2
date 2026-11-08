"""Pydantic v2 request and response schemas (kept separate from the ORM model)."""

from pydantic import BaseModel, ConfigDict


class ItemOut(BaseModel):
    """Response schema. Provided."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    name: str
    description: str | None
    price: float
    stock: int


class ItemCreate(BaseModel):
    """Request body of POST /items.

    TODO (AC 2): declare the fields `sku`, `name`, `description` (optional), `price` and
    `stock` (default 0) with validation: `sku` and `name` must not be empty, `price` and `stock`
    must be >= 0. Invalid input must produce a 422 response (use `Field(...)` constraints).
    """


class ItemUpdate(BaseModel):
    """Request body of PATCH /items/{item_id}: every field is optional.

    TODO (AC 2): declare `name`, `description`, `price` and `stock`, all optional, with the same
    constraints as ItemCreate. The `sku` cannot be changed.
    """
