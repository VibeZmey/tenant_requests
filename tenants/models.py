from django.db import models
from django.urls import reverse


class Tenant(models.Model):
    name = models.CharField("Имя", max_length=200)
    flat = models.PositiveIntegerField("Квартира")
    phone = models.CharField("Телефон", max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = "жилец"
        verbose_name_plural = "жильцы"
        ordering = ("flat", "pk")
        constraints = [
            models.CheckConstraint(condition=models.Q(flat__gt=0), name="tenant_flat_positive"),
        ]

    def __str__(self):
        return f"{self.name} (кв. {self.flat})"

    def get_absolute_url(self):
        return reverse("tenants:tenant_detail", args=[self.pk])
