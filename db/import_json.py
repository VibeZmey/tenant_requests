"""Запуск из корня: python -m db.import_json. Повторный импорт безопасен."""
import argparse
import json
from datetime import date
from pathlib import Path

from db.database import BASE_DIR, DB_PATH, connect


def import_data(source=None, destination=None):
    source = Path(source or BASE_DIR / "data")
    destination = Path(destination or DB_PATH)
    records = {
        name: json.loads((source / (name + ".json")).read_text(encoding="utf-8"))
        for name in ("tenants", "executors", "requests")
    }
    for item in records["requests"]:
        date.fromisoformat(item["date"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    with connect(destination) as conn:
        conn.executescript((BASE_DIR / "sql/schema.sql").read_text(encoding="utf-8"))
        # Схема создается отдельно; данные заменяются одной транзакцией.
        conn.execute("BEGIN")
        conn.execute("DELETE FROM requests")
        conn.execute("DELETE FROM tenants")
        conn.execute("DELETE FROM executors")
        conn.executemany(
            "INSERT INTO tenants(id,name,flat,phone) VALUES (?,?,?,?)",
            [(i["id"], i["name"], i["flat"], i.get("phone")) for i in records["tenants"]],
        )
        conn.executemany(
            "INSERT INTO executors(id,name,specialization,is_busy) "
            "VALUES (?,?,?,?)",
            [(i["id"], i["name"], i["specialization"], i["is_busy"])
             for i in records["executors"]],
        )
        conn.executemany(
            "INSERT INTO requests(id,tenant_id,problem,date,category,status,executor_id) "
            "VALUES (?,?,?,?,?,?,?)",
            [(i["id"], i["tenant_id"], i["problem"], i["date"], i["category"],
              i["status"], i.get("executor_id")) for i in records["requests"]],
        )
        conn.commit()
    return {name: len(items) for name, items in records.items()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--database", type=Path)
    args = parser.parse_args()
    print(import_data(args.source, args.database))
