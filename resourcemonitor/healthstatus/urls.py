from django.urls import path
from . import views

urlpatterns = [
    path("devices", views.callDeviceService, name="API"), # Direct API access
    path("", views.frontEnd, name="Network Health Monitor"), # Live Status Viewer
    path("dashboard", views.metricsDashboard, name="Dashboard"), # Plotly Metrics Dashboard
]
