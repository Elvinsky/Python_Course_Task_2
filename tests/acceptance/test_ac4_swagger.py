"""AC 4: interactive Swagger docs at /docs and a properly documented OpenAPI schema."""

import re
from typing import Any

import pytest
from httpx import AsyncClient

from app.main import app

EXPECTED = {
    ("get", "/items"),
    ("get", "/items/{id}"),
    ("post", "/items"),
    ("patch", "/items/{id}"),
    ("delete", "/items/{id}"),
}


def _operations() -> dict[tuple[str, str], dict[str, Any]]:
    schema = app.openapi()
    operations: dict[tuple[str, str], dict[str, Any]] = {}
    for path, methods in schema["paths"].items():
        for method, operation in methods.items():
            operations[(method, re.sub(r"\{[^}]+\}", "{id}", path))] = operation
    return operations


async def test_swagger_ui_is_served_at_docs(client: AsyncClient) -> None:
    response = await client.get("/docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower()


async def test_openapi_schema_is_served(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")

    assert response.status_code == 200 and "paths" in response.json()


def test_all_five_operations_are_documented() -> None:
    assert EXPECTED <= set(_operations()), (
        f"missing operations: {sorted(EXPECTED - set(_operations()))}"
    )


def test_post_documents_201_and_its_request_body_fields() -> None:
    operation = _operations()[("post", "/items")]
    assert "201" in operation["responses"], "set status_code=201 on POST /items"
    ref = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    schema = app.openapi()["components"]["schemas"][ref.rsplit("/", 1)[-1]]
    assert {"sku", "name", "price"} <= set(schema.get("properties", {})), (
        "declare the fields on ItemCreate"
    )


def test_patch_documents_a_request_body_with_optional_fields() -> None:
    operation = _operations()[("patch", "/items/{id}")]
    ref = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    schema = app.openapi()["components"]["schemas"][ref.rsplit("/", 1)[-1]]
    assert {"name", "description", "price", "stock"} <= set(schema.get("properties", {})), (
        "declare the fields on ItemUpdate"
    )
    assert not schema.get("required"), "every ItemUpdate field must be optional"


def test_delete_documents_204() -> None:
    assert "204" in _operations()[("delete", "/items/{id}")]["responses"], (
        "set status_code=204 on DELETE"
    )


@pytest.mark.parametrize(
    "operation", [("get", "/items/{id}"), ("patch", "/items/{id}"), ("delete", "/items/{id}")]
)
def test_item_operations_document_404(operation: tuple[str, str]) -> None:
    assert "404" in _operations()[operation]["responses"], (
        'add responses={404: {"description": "Item not found"}}'
    )


def test_post_documents_409() -> None:
    assert "409" in _operations()[("post", "/items")]["responses"], (
        "document the duplicate-sku 409 on POST"
    )
