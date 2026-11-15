from django.contrib import admin

from .models import Request


class RequestInline(admin.TabularInline):
    model = Request
    extra = 0
    fields = ("tenant", "executor", "date", "category", "problem", "status")
    show_change_link = True


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant", "executor", "category", "date", "status")
    list_display_links = ("id",)
    list_filter = ("status", "date", "category")
    search_fields = ("problem", "tenant__name", "executor__name")
    list_select_related = ("tenant", "executor")
    ordering = ("-date", "-pk")
    date_hierarchy = "date"
    list_per_page = 20
