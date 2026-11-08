"""AC 6: your own pytest tests (httpx.AsyncClient) cover all five endpoints incl. 404 and 422.

This meta test inspects tests/test_items.py. It cannot judge quality, only the basics.
"""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREE = ast.parse((ROOT / "tests" / "test_items.py").read_text())


def _client_methods() -> set[str]:
    return {
        node.func.attr
        for node in ast.walk(TREE)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "client"
    }


def _integers() -> set[int]:
    return {
        n.value for n in ast.walk(TREE) if isinstance(n, ast.Constant) and isinstance(n.value, int)
    }


def test_has_at_least_eight_tests() -> None:
    tests = [
        n
        for n in ast.walk(TREE)
        if isinstance(n, ast.AsyncFunctionDef | ast.FunctionDef) and n.name.startswith("test_")
    ]
    assert len(tests) >= 8, (
        f"found {len(tests)} test functions in tests/test_items.py; write at least 8"
    )


def test_exercises_all_four_http_methods_through_the_client() -> None:
    missing = {"get", "post", "patch", "delete"} - _client_methods()
    assert not missing, f"tests/test_items.py never calls client.{sorted(missing)}"


def test_covers_the_error_cases() -> None:
    assert {404, 422} <= _integers(), (
        "assert a 404 (unknown id) and a 422 (invalid body) in tests/test_items.py"
    )
