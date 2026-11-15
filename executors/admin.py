from django.contrib import admin

from requests.admin import RequestInline

from .models import Executor


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "is_busy")
    list_editable = ("is_busy",)
    list_filter = ("is_busy", "specialization")
    search_fields = ("name", "specialization")
    ordering = ("name", "pk")
    list_per_page = 20
    inlines = (RequestInline,)
