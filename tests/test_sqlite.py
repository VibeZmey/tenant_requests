"""Проверки ПР7 на изолированной базе, без изменения данных проекта."""
import json
import sqlite3

import pytest

from db.database import BASE_DIR, QUERIES, connect, fetch
from db.import_json import import_data


@pytest.fixture
def database(tmp_path, monkeypatch):
    path = tmp_path / "test.sqlite"
    import_data(destination=path)
    monkeypatch.setenv("TENANT_REQUESTS_DB", str(path))
    return path


def test_import_idempotent_and_relations(database):
    import_data(destination=database)
    with connect(database) as conn:
        for table in ("tenants", "executors", "requests"):
            expected = json.loads((BASE_DIR / "data" / (table + ".json")).read_text("utf-8"))
            assert conn.execute("SELECT COUNT(*) FROM " + table).fetchone()[0] == len(expected)
        assert not conn.execute("PRAGMA foreign_key_check").fetchall()
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("UPDATE requests SET tenant_id = -100 WHERE id = 1")


def test_queries_and_null_join(database):
    assert len(QUERIES) >= 10
    assert len(fetch("tenants", (20, 0))) == 2
    assert fetch("tenant_search", ("%", "109"))
    assert not fetch("tenant_search", ("%' OR 1=1 --%", "' OR 1=1 --"))
    assert len(fetch("available_executors", ("сантехника", "сантехника"))) == 1
    assert not fetch("available_executors", ("электрика", "электрика"))
    assert len(fetch("requests", ("", "", "", ""))) == 2
    assert fetch("request_detail", (2,), one=True)["executor_name"] is None
    assert len(fetch("tenant_requests", (1,))) == 2
    assert fetch("request_totals", one=True)["unassigned"] == 1
    assert fetch("executor_totals", one=True)["total"] == 2
    assert len(fetch("category_stats")) == 2
    assert len(fetch("executor_stats", (0,))) == 2
    assert not fetch("executor_stats", (100,))


def test_failed_import_rolls_back(database, tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    for name in ("tenants", "executors", "requests"):
        items = json.loads((BASE_DIR / "data" / (name + ".json")).read_text("utf-8"))
        if name == "requests":
            items[0]["tenant_id"] = -100
        (source / (name + ".json")).write_text(json.dumps(items), "utf-8")
    with pytest.raises(sqlite3.IntegrityError):
        import_data(source, database)
    assert fetch("request_detail", (1,), one=True)["tenant_id"] == 1
