from django.db import models
from django.urls import reverse

ACTIVE_STATUSES = ("Новая", "В работе")


class Request(models.Model):
    tenant = models.ForeignKey(
        "tenants.Tenant", models.PROTECT, related_name="requests", verbose_name="Жилец",
    )
    executor = models.ForeignKey(
        "executors.Executor", models.PROTECT, related_name="requests",
        verbose_name="Исполнитель", null=True, blank=True,
    )
    problem = models.TextField("Проблема")
    date = models.DateField("Дата")
    category = models.CharField("Категория", max_length=120)
    status = models.CharField("Статус", max_length=20, default="Новая")

    class Meta:
        ordering = ("-date", "-pk")
        indexes = [models.Index(fields=["category", "status"])]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=(*ACTIVE_STATUSES, "Выполнена", "Отменена")),
                name="request_status_valid",
            ),
        ]

    def __str__(self):
        return f"Заявка №{self.pk}"

    def get_absolute_url(self):
        return reverse("requests:request_detail", args=[self.pk])


def request_rows(queryset):
    return queryset.annotate(
        tenant_name=models.F("tenant__name"), flat=models.F("tenant__flat"),
        executor_name=models.F("executor__name"),
    ).values(
        "id", "problem", "date", "category", "status", "tenant_id", "executor_id",
        "tenant_name", "flat", "executor_name",
    )
