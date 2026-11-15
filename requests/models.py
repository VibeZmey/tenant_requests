from django.db import models
from django.urls import reverse


class RequestStatus(models.TextChoices):
    NEW = "new", "Новая"
    IN_PROGRESS = "in_progress", "В работе"
    COMPLETED = "completed", "Выполнена"
    CANCELLED = "cancelled", "Отменена"


ACTIVE_STATUSES = (RequestStatus.NEW, RequestStatus.IN_PROGRESS)
LEGACY_STATUS_CODES = {label: code for code, label in RequestStatus.choices}


class RequestQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=ACTIVE_STATUSES)

    def cancelled(self):
        return self.filter(status=RequestStatus.CANCELLED)

    def completed(self):
        return self.filter(status=RequestStatus.COMPLETED)

    def for_date(self, day):
        return self.filter(date=day)


class Request(models.Model):
    Status = RequestStatus

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
    status = models.CharField("Статус", max_length=20, choices=Status, default=Status.NEW)

    objects = RequestQuerySet.as_manager()

    class Meta:
        verbose_name = "заявка"
        verbose_name_plural = "заявки"
        ordering = ("-date", "-pk")
        indexes = [models.Index(fields=["category", "status"])]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=RequestStatus.values),
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
