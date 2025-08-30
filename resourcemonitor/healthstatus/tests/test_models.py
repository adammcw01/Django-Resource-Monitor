"""
This file is a test suite for the data models as part of the healthstatus app.
"""
import pytest
from django.utils import timezone
from healthstatus.models import DeviceStatus, SystemMetric


@pytest.mark.django_db
def testDeviceStatus():
    """
    Test object creation and retrieval for DeviceStatus model.
    """
    device = DeviceStatus.objects.create(
        device_id=1,
        name="Router01",
        ip_address="192.168.1.1",
        status=True
    )

    assert isinstance(device, DeviceStatus)
    assert device.device_id == 1
    assert device.name == "Router01"
    assert device.ip_address == "192.168.1.1"
    assert device.status is True
    assert device.timestamp <= timezone.now()

@pytest.mark.django_db
def testSystemMetric():
    """
    Test object creation and retrieval for SystemMetric model.
    """
    metric = SystemMetric.objects.create(
        endpoint="/devices",
        status_code=200,
        success=True
    )

    assert isinstance(metric, SystemMetric)
    assert metric.endpoint == "/devices"
    assert metric.status_code == 200
    assert metric.success is True
    assert metric.timestamp <= timezone.now()
