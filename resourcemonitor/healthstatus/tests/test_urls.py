"""
This file is a test suite for the url routing as part of the healthstatus app.
"""
import pytest
from django.urls import reverse, resolve
from healthstatus import views


def testDevicesResolution():
    """
    Test that the /devices URL resolves to the correct view.
    """
    path = reverse("API")
    assert resolve(path).func == views.callDeviceService

def testIndexResolution():
    """
    Test that the root URL resolves to the frontEnd view.
    """
    path = reverse("Network Health Monitor")
    assert resolve(path).func == views.frontEnd

def testDashboardResolution():
    """
    Test that the /dashboard URL resolves to the metricsDashboard view.
    """
    path = reverse("Dashboard")
    assert resolve(path).func == views.metricsDashboard
