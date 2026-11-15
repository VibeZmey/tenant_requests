from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

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

    def test_status_and_executor_availability(self):
        req = Request.objects.select_related("executor").get(pk=1)
        executor = req.executor
        executor.is_busy = False
        executor.save(update_fields=["is_busy"])
        req.status = Request.Status.IN_PROGRESS
        req.save(update_fields=["status"])
        params = {"available": "1", "date": req.date.isoformat()}
        response = self.client.get("/executors/", params)
        self.assertNotContains(response, executor.name)
        self.assertContains(response, 'value="1"')
        self.assertContains(
            self.client.get("/executors/", {**params, "date": "2025-01-01"}), executor.name,
        )
        for status in (Request.Status.CANCELLED, Request.Status.COMPLETED):
            req.status = status
            req.save(update_fields=["status"])
            self.assertContains(self.client.get("/executors/", params), executor.name)
        self.assertTrue(Request.objects.completed().for_date(req.date).filter(pk=req.pk).exists())
        self.assertContains(self.client.get("/requests/", {"status": "Выполнена"}), req.problem)
        self.assertContains(self.client.get("/requests/statistics/"), "Выполнено: 1")

    def test_executor_slug_and_legacy_url(self):
        executor = Executor.objects.get(pk=1)
        self.assertContains(self.client.get("/executors/"), executor.get_absolute_url())
        self.assertContains(self.client.get(executor.get_absolute_url()), executor.name)
        self.assertContains(self.client.get("/executors/1/"), executor.name)
        self.assertEqual(self.client.get("/executors/profile/nonexistent/").status_code, 404)


class RequestAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_user_model().objects
        cls.admin = users.create_superuser("test-admin")
        cls.staff = users.create_user("test-staff", is_staff=True)
        group = Group.objects.create(name="Операторы")
        group.permissions.set(Permission.objects.filter(
            content_type__app_label="executors", codename__in=(
                "view_executor", "add_executor", "change_executor",
            ),
        ))
        cls.staff.groups.add(group)
        cls.tenant = Tenant.objects.create(name="Жилец для проверки", flat=12)
        cls.executor = Executor.objects.create(name="Мастер", specialization="Учебная")
        cls.req = Request.objects.create(
            tenant=cls.tenant, executor=cls.executor, date="2026-06-01",
            category="Учебная", problem="Проверка Django Admin",
        )

    def test_admin_search_inline_and_status_edit(self):
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse("admin:index")), "Исполнители")
        response = self.client.get(reverse("admin:requests_request_changelist"), {
            "q": self.tenant.name, "status__exact": Request.Status.NEW,
        })
        self.assertContains(response, str(self.tenant))
        for name, obj in (("tenants_tenant", self.tenant), ("executors_executor", self.executor)):
            url = reverse(f"admin:{name}_change", args=[obj.pk])
            self.assertContains(self.client.get(url), self.req.problem)

        url = reverse("admin:requests_request_change", args=[self.req.pk])
        response = self.client.post(url, {
            "tenant": self.tenant.pk, "executor": self.executor.pk,
            "date": "2026-06-01", "category": "Учебная", "problem": self.req.problem,
            "status": Request.Status.CANCELLED, "_save": "Сохранить",
        })
        self.assertEqual(response.status_code, 302)
        self.req.refresh_from_db()
        self.assertEqual(self.req.status, Request.Status.CANCELLED)
        self.assertTrue(Request.objects.cancelled().filter(pk=self.req.pk).exists())
        self.assertContains(self.client.get(self.req.get_absolute_url()), "Отменена")
        self.assertContains(self.client.get("/requests/statistics/"), "Отменено: 1")

    def test_permissions_and_protected_delete(self):
        url = reverse("admin:executors_executor_delete", args=[self.executor.pk])
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.staff)
        for action in ("changelist", "add"):
            self.assertEqual(
                self.client.get(reverse(f"admin:executors_executor_{action}")).status_code, 200,
            )
        edit = reverse("admin:executors_executor_change", args=[self.executor.pk])
        self.assertEqual(self.client.get(edit).status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(url), str(self.req))
        self.assertTrue(Executor.objects.filter(pk=self.executor.pk).exists())
