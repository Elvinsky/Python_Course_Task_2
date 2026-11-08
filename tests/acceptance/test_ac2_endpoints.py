"""AC 2: REST endpoints GET /items, GET /items/{id}, POST /items, PATCH and DELETE /items/{id}."""

from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models import Item

PAYLOAD: dict[str, Any] = {
    "sku": "TEST-001",
    "name": "Test Widget",
    "description": "A widget for tests",
    "price": 9.99,
    "stock": 5,
}


async def _insert(factory: async_sessionmaker[AsyncSession], **overrides: Any) -> int:
    values = {**PAYLOAD, **overrides}
    async with factory() as session:
        item = Item(**values)
        session.add(item)
        await session.commit()
        return item.id


async def test_list_items_returns_items_ordered_by_id(
    client: AsyncClient, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    await _insert(session_factory, sku="B-1", name="B")
    await _insert(session_factory, sku="A-1", name="A")

    response = await client.get("/items")

    assert response.status_code == 200
    assert [item["sku"] for item in response.json()] == ["B-1", "A-1"]


async def test_get_item_returns_the_item(
    client: AsyncClient, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    item_id = await _insert(session_factory)

    response = await client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json() == {"id": item_id, **PAYLOAD}


async def test_get_unknown_item_returns_404(client: AsyncClient) -> None:
    assert (await client.get("/items/999999")).status_code == 404


async def test_create_item_returns_201_and_persists(client: AsyncClient) -> None:
    response = await client.post("/items", json=PAYLOAD)

    assert response.status_code == 201, response.text
    created = response.json()
    assert created["id"] > 0 and created["sku"] == PAYLOAD["sku"]
    assert (await client.get(f"/items/{created['id']}")).json() == created


async def test_create_item_defaults_stock_to_zero(client: AsyncClient) -> None:
    response = await client.post(
        "/items", json={"sku": "NO-STOCK", "name": "No stock", "price": 1.5}
    )

    assert response.status_code == 201, response.text
    assert response.json()["stock"] == 0 and response.json()["description"] is None


async def test_create_item_with_duplicate_sku_returns_409(client: AsyncClient) -> None:
    assert (await client.post("/items", json=PAYLOAD)).status_code == 201

    assert (await client.post("/items", json=PAYLOAD)).status_code == 409


@pytest.mark.parametrize(
    "override",
    [
        {"name": ""},
        {"sku": ""},
        {"price": -1},
        {"stock": -5},
        {"price": "free"},
        {"stock": 1.5},
    ],
)
async def test_create_item_rejects_invalid_input_with_422(
    client: AsyncClient, override: dict[str, Any]
) -> None:
    response = await client.post("/items", json={**PAYLOAD, **override})

    assert response.status_code == 422, response.text


@pytest.mark.parametrize("missing", ["sku", "name", "price"])
async def test_create_item_requires_sku_name_and_price(client: AsyncClient, missing: str) -> None:
    body = {key: value for key, value in PAYLOAD.items() if key != missing}

    assert (await client.post("/items", json=body)).status_code == 422


async def test_patch_updates_only_the_given_fields(
    client: AsyncClient, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    item_id = await _insert(session_factory)

    response = await client.patch(f"/items/{item_id}", json={"price": 12.5})

    assert response.status_code == 200, response.text
    assert response.json() == {"id": item_id, **PAYLOAD, "price": 12.5}
    assert (await client.get(f"/items/{item_id}")).json()["price"] == 12.5, (
        "PATCH must be committed"
    )


async def test_patch_can_set_description_to_null(
    client: AsyncClient, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    item_id = await _insert(session_factory)

    response = await client.patch(f"/items/{item_id}", json={"description": None})

    assert response.status_code == 200 and response.json()["description"] is None


async def test_patch_with_empty_body_changes_nothing(
    client: AsyncClient, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    item_id = await _insert(session_factory)

    response = await client.patch(f"/items/{item_id}", json={})

    assert response.status_code == 200 and response.json() == {"id": item_id, **PAYLOAD}


async def test_patch_unknown_item_returns_404(client: AsyncClient) -> None:
    assert (await client.patch("/items/999999", json={"price": 1})).status_code == 404


@pytest.mark.parametrize("body", [{"price": -1}, {"stock": -1}, {"name": ""}])
async def test_patch_rejects_invalid_input_with_422(
    client: AsyncClient, session_factory: async_sessionmaker[AsyncSession], body: dict[str, Any]
) -> None:
    item_id = await _insert(session_factory)

    assert (await client.patch(f"/items/{item_id}", json=body)).status_code == 422


async def test_delete_returns_204_and_removes_the_item(
    client: AsyncClient, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    item_id = await _insert(session_factory)

    response = await client.delete(f"/items/{item_id}")

    assert response.status_code == 204 and response.content == b""
    assert (await client.get(f"/items/{item_id}")).status_code == 404


async def test_delete_unknown_item_returns_404(client: AsyncClient) -> None:
    assert (await client.delete("/items/999999")).status_code == 404
