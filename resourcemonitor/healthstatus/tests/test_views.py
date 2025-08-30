"""
This file is a test suite for the healthstatus app views.
"""
import pytest
from django.http import HttpRequest
from django.urls import reverse
from healthstatus import views
import json

@pytest.mark.django_db
def testCallDeviceService(mocker):
    """
    Test that callDeviceService fetches devices.
    Saves them to the database.
    Creates logs in another database.
    """
    # Create a fake response to remove dependency on Flask API.
    mockResp = mocker.Mock()
    mockResp.status_code = 200
    mockResp.json.return_value = [
        {"id": 1, "name": "Router", "ip_address": "192.168.0.1", "status": True}
    ]
    mockResp.raise_for_status.return_value = None
    mocker.patch("healthstatus.views.requests.get", return_value=mockResp)

    # Create a new entry from the mock object.
    mockRecord = mocker.patch("healthstatus.views.DeviceStatus.objects.create")

    mockLog = mocker.patch("healthstatus.views.generateLog")

    request = HttpRequest()
    response = views.callDeviceService(request)

    assert response.status_code == 200
    assert json.loads(response.content) == mockResp.json.return_value
    mockRecord.assert_called_once_with(
        device_id=1,
        name="Router",
        ip_address="192.168.0.1",
        status=True
    )
    mockLog.assert_called_once_with("/devices", 200, True)


@pytest.mark.django_db
def testCallDeviceServiceError(mocker):
    """
    Test that callDeviceService handles exceptions and logs failure.
    """
    mocker.patch("healthstatus.views.requests.get", side_effect=Exception("Failed To Fetch Devices"))
    mockLog = mocker.patch("healthstatus.views.generateLog")

    request = HttpRequest()
    response = views.callDeviceService(request)

    assert response.status_code == 500
    assert "error" in json.loads(response.content)
    mockLog.assert_called_once()
    args, kwargs = mockLog.call_args
    assert args[0] == "/devices"
    assert args[2] is False


@pytest.mark.django_db
def testFrontEndRender(mocker):
    """
    Test that frontEnd renders the template, and generates a log.
    """
    mockLog = mocker.patch("healthstatus.views.generateLog")
    mockRender = mocker.patch("healthstatus.views.render", return_value="rendered")

    request = HttpRequest()
    result = views.frontEnd(request)

    assert result == "rendered"
    mockLog.assert_called_once_with("/index", 200, True)
    mockRender.assert_called_once_with(request, "devices.html")

@pytest.mark.django_db
def testMetricsDashboardEmpty(mocker):
    """
    Test that metricsDashboard returns 'No system metrics yet' when db is empty.
    """
    mocker.patch("healthstatus.views.generateLog")
    mocker.patch("healthstatus.views.getAvailTable", return_value="<table>mock</table>")
    mocker.patch("healthstatus.views.SystemMetric.objects.values", return_value=[])

    mockRender = mocker.patch("healthstatus.views.render", return_value="rendered")

    request = HttpRequest()
    result = views.metricsDashboard(request)

    assert result == "rendered"
    args, kwargs = mockRender.call_args
    context = args[2]
    assert "<p>No system metrics yet</p>" in context["system_chart"]


@pytest.mark.django_db
def testMetricsDashboard(mocker):
    """
    Test that metricsDashboard renders metrics.html with table and chart when data exists.
    """
    mocker.patch("healthstatus.views.generateLog")
    mocker.patch("healthstatus.views.getAvailTable", return_value="<table>mock</table>")

    # Mock SystemMetric.objects.values to return data
    mocker.patch(
        "healthstatus.views.SystemMetric.objects.values",
        return_value=[
            {"timestamp": "2025-08-30T12:00:00Z", "endpoint": "/devices", "success": True}
        ]
    )

    mockRender = mocker.patch("healthstatus.views.render", return_value="rendered")

    request = HttpRequest()
    result = views.metricsDashboard(request)

    assert result == "rendered"
    args, kwargs = mockRender.call_args
    assert args[1] == "metrics.html"
    context = args[2]
    assert "<table>mock</table>" in context["table"]
    assert "system_chart" in context


