from django.urls import path
from . import views

urlpatterns = [
    path("devices", views.callDeviceService, name="devices_api"),
    path("", views.frontEnd, name="devices_page"),
    path("metrics", views.metrics, name="metrics"),
]
