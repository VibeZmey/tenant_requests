from django.urls import path
from . import views

app_name = "tenants"

urlpatterns = [
    path("", views.tenant_list, name="tenant_list"),
    path("<int:tenant_id>/", views.tenant_detail, name="tenant_detail"),
]