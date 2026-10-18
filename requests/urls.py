from django.urls import path
from . import views

urlpatterns = [
    path("", views.request_list, name="request_list"),
    path("<int:request_id>/", views.request_detail, name="request_detail"),
]