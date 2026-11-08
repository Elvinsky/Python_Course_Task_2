"""Your own tests for the items API (AC 6). This file is yours; acceptance tests never replace it.

Use the `client` fixture from conftest.py (an `httpx.AsyncClient` talking to the app in-process).
"""

from httpx import AsyncClient


async def test_list_items_is_empty_for_a_fresh_database(client: AsyncClient) -> None:
    response = await client.get("/items")

    assert response.status_code == 200
    assert response.json() == []


# TODO (AC 6): write tests for ALL five endpoints with httpx.AsyncClient (the `client` fixture),
# including the error cases. The meta test tests/acceptance/test_ac6_own_tests.py checks that
# this file:
#   * calls client.get, client.post, client.patch and client.delete,
#   * expects 404 (unknown id) and 422 (invalid body) somewhere, and
#   * contains at least 8 test functions.
# Ideas: create then read back, duplicate sku, a partial update leaves other fields untouched,
# delete then 404.
