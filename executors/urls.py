from django.urls import path
from . import views

urlpatterns = [
    path("", views.executor_list, name="executor_list"),
    path("<int:executor_id>/", views.executor_detail, name="executor_detail"),
]