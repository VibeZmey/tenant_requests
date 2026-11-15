from django.contrib import admin

from requests.admin import RequestInline

from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "flat", "phone")
    list_filter = ("flat",)
    search_fields = ("name", "phone", "=flat")
    ordering = ("flat", "pk")
    list_per_page = 20
    inlines = (RequestInline,)
