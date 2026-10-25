from django.urls import path
from . import views

app_name = "requests"

urlpatterns = [
    path("statistics/", views.statistics, name="statistics"),
    path("", views.request_list, name="request_list"),
    path("<int:request_id>/", views.request_detail, name="request_detail"),
]
