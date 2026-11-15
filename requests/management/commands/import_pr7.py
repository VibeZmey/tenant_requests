import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, transaction

from executors.models import Executor
from requests.models import LEGACY_STATUS_CODES, Request
from tenants.models import Tenant


class Command(BaseCommand):
    help = "Переносит данные ПР7 из SQLite в базу Django с сохранением ID и связей."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source", type=Path, default=settings.BASE_DIR / "data/tenant_requests.sqlite",
        )

    def handle(self, *args, **options):
        source = options["source"].resolve()
        try:
            with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as legacy:
                legacy.row_factory = sqlite3.Row
                legacy.execute("BEGIN")
                with transaction.atomic():
                    for model, table in (
                        (Tenant, "tenants"), (Executor, "executors"), (Request, "requests"),
                    ):
                        for row in legacy.execute(f"SELECT * FROM {table} ORDER BY id"):
                            self.import_row(model, dict(row))
        except (sqlite3.Error, DatabaseError, ValueError) as exc:
            raise CommandError(f"Перенос не выполнен: {exc}") from exc
        self.stdout.write(self.style.SUCCESS("Данные ПР7 перенесены."))

    @staticmethod
    def import_row(model, values):
        pk = values.pop("id")
        if model is Request:
            values["date"] = date.fromisoformat(values["date"])
            values["status"] = LEGACY_STATUS_CODES.get(values["status"], values["status"])
        elif model is Executor:
            values["is_busy"] = bool(values["is_busy"])
        obj, created = model.objects.get_or_create(pk=pk, defaults=values)
        if not created and any(getattr(obj, key) != value for key, value in values.items()):
            raise CommandError(f"{model.__name__} №{pk} уже существует с другими данными.")
