"""AC 5: the schema comes from an Alembic migration (`alembic upgrade head`), not `create_all`."""

import sqlite3
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

ROOT = Path(__file__).resolve().parents[2]


def _config(database: Path) -> Config:
    config = Config(str(ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{database}")
    return config


def test_a_migration_revision_exists() -> None:
    revisions = [p for p in (ROOT / "alembic" / "versions").glob("*.py") if p.name != "__init__.py"]
    assert revisions, 'generate it: uv run alembic revision --autogenerate -m "create items"'


def test_upgrade_head_creates_the_items_table(tmp_path: Path) -> None:
    database = tmp_path / "migrated.db"
    command.upgrade(_config(database), "head")

    with sqlite3.connect(database) as connection:
        tables = {
            row[0]
            for row in connection.execute("select name from sqlite_master where type = 'table'")
        }
        columns = {row[1] for row in connection.execute("pragma table_info(items)")}
    assert {"items", "alembic_version"} <= tables
    assert {"id", "sku", "name", "description", "price", "stock"} <= columns


def test_migrated_schema_enforces_unique_sku(tmp_path: Path) -> None:
    database = tmp_path / "unique.db"
    command.upgrade(_config(database), "head")

    with sqlite3.connect(database) as connection:
        insert = "insert into items (sku, name, price, stock) values ('X-1', 'Name', 1.0, 0)"
        connection.execute(insert)
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(insert)


def _tables(database: Path) -> set[str]:
    with sqlite3.connect(database) as connection:
        rows = connection.execute("select name from sqlite_master where type = 'table'")
        return {row[0] for row in rows}


def test_downgrade_removes_the_items_table(tmp_path: Path) -> None:
    database = tmp_path / "down.db"
    config = _config(database)
    command.upgrade(config, "head")
    assert "items" in _tables(database), "upgrade head must create the items table first"

    command.downgrade(config, "base")

    assert "items" not in _tables(database), "downgrade() must drop what upgrade() created"


def test_application_code_does_not_use_create_all() -> None:
    offenders = [
        str(path.relative_to(ROOT))
        for folder in ("app", "scripts")
        for path in (ROOT / folder).rglob("*.py")
        if "create_all" in path.read_text()
    ]
    assert not offenders, f"use Alembic migrations instead of create_all in: {offenders}"
