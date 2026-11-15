from uuid import uuid4

from django.db import models
from django.urls import reverse


def executor_slug():
    return f"executor-{uuid4().hex}"


class Executor(models.Model):
    name = models.CharField("Имя", max_length=200)
    specialization = models.CharField("Специализация", max_length=120)
    is_busy = models.BooleanField("Занят", default=False)
    slug = models.SlugField("Код в адресе", unique=True, default=executor_slug)

    class Meta:
        verbose_name = "исполнитель"
        verbose_name_plural = "исполнители"
        ordering = ("name", "pk")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("executors:executor_by_slug", kwargs={"slug": self.slug})
