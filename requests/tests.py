from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.db.models import ProtectedError
from django.test import TestCase

from db.import_json import import_data
from executors.models import Executor
from tenants.models import Tenant

from .models import Request


class RequestPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        with TemporaryDirectory() as folder:
            source = Path(folder) / "pr7.sqlite"
            import_data(destination=source)
            call_command("import_pr7", source=source)
            call_command("import_pr7", source=source)

    def test_preserved_data_and_pages(self):
        counts = (Tenant.objects.count(), Executor.objects.count(), Request.objects.count())
        self.assertEqual(counts, (2, 2, 2))
        first, second = Request.objects.order_by("pk")
        self.assertEqual(first.tenant_id, 1)
        self.assertIsNone(second.executor_id)
        with self.assertRaises(ProtectedError):
            first.tenant.delete()
        for url in ("/", "/tenants/", "/tenants/1/", "/executors/", "/executors/1/",
                    "/requests/", "/requests/1/",
                    "/tenants/?page=bad", "/executors/?available=1",
                    "/requests/statistics/?minimum=bad"):
            self.assertEqual(self.client.get(url).status_code, 200, url)
        for url in ("/tenants/999/", "/executors/999/", "/requests/999/"):
            self.assertEqual(self.client.get(url).status_code, 404, url)
        self.assertContains(self.client.get("/requests/2/"), "Не назначен")
        self.assertContains(self.client.get("/requests/"), "Петров")
        self.assertContains(self.client.get("/tenants/?q=нет"), "Жильцы не найдены")
        self.assertContains(self.client.get("/requests/?category=нет"), "Заявки не найдены")
        response = self.client.get("/executors/", {"available": 1, "specialization": "сантехника"})
        self.assertContains(response, "Сидоров")
        self.assertNotContains(self.client.get("/executors/?available=1"), "Петров")
        Request.objects.all().delete()
        Executor.objects.all().delete()
        self.assertContains(self.client.get("/requests/statistics/"), "Всего заявок: 0")

    def test_filters_sorting_and_pagination(self):
        day = date(2026, 1, 2)
        Request.objects.bulk_create([
            Request(tenant_id=1, problem=f"Проверка {i}", date=day, category="Тест")
            for i in range(12)
        ])
        params = {"category": "Тест", "date": day.isoformat(), "tenant": "1", "sort": "oldest"}
        with self.assertNumQueries(2):
            response = self.client.get("/requests/", params)
        self.assertEqual(len(response.context["page_obj"]), 10)
        self.assertContains(response, "sort=oldest&amp;page=2")
        response = self.client.get("/requests/", {**params, "page": "2"})
        self.assertEqual([r["problem"] for r in response.context["page_obj"]],
                         ["Проверка 10", "Проверка 11"])
        response = self.client.get("/requests/", {**params, "date": "bad", "sort": "bad"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context["form"].errors), {"date", "sort"})
        self.assertEqual(response.context["page_obj"][0]["problem"], "Проверка 11")
        with self.assertNumQueries(1):
            self.assertContains(self.client.get("/requests/1/"), "Петров")
