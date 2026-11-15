from django.db import models
from django.urls import reverse


class Executor(models.Model):
    name = models.CharField("Имя", max_length=200)
    specialization = models.CharField("Специализация", max_length=120)
    is_busy = models.BooleanField("Занят", default=False)

    class Meta:
        ordering = ("name", "pk")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("executors:executor_detail", args=[self.pk])
