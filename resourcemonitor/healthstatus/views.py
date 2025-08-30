from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
import requests
import logging
from healthstatus.models import DeviceStatus, SystemMetric
import plotly.express as px
import pandas as pd
from .utils import generateLog, getDeviceAvail, getAvailTable
import plotly.graph_objects as go
from django.utils.safestring import mark_safe
from typing import List
import os

logger = logging.getLogger(__name__)

def callDeviceService(request: HttpRequest) -> JsonResponse:
    """
    Fetch devices from Flask API and record response in SQLite.

    Args:
        request (HttpRequest): The HTTP request.
    
    Returns:
        JsonResponse: The JSON response containing device data or error information.
    """

    # Determine if Django is running as part of Docker compose or not
    if os.getenv("RUN_ENV") == "docker":
        DEVICE_API_URL = "http://network_devices_api:8000/devices" # Address of dependant container.
    else:
        DEVICE_API_URL = "http://127.0.0.1:8000/devices" # Fallback for local instances.

    try:
        resp: requests.Response = requests.get(DEVICE_API_URL, timeout=5)
        resp.raise_for_status()
        devices: List[dict] = resp.json()
    
        for d in devices:
            DeviceStatus.objects.create(
                device_id=d["id"],
                name=d["name"],
                ip_address=d["ip_address"],
                status=d["status"],
            )

        generateLog("/devices", resp.status_code, True) # Store status in DeviceStatus

        logger.info("Stored %d device records", len(devices))
        return JsonResponse(devices, safe=False)

    except Exception as e:
        logger.error("Error fetching device data: %s", e)
        status = getattr(getattr(e, "response", None), "status_code", 500) # Log none if empty response.
        generateLog("/devices", status, False) # Record error in SystemMetric
        return JsonResponse({"error": str(e)}, status=500)


def frontEnd(request: HttpRequest) -> JsonResponse:
    """
    Serve the front end to the client.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        JsonResponse: The JSON response containing device data or error information.
    """
    generateLog("/index", 200, True) # Record serve in SystemMetric
    return render(request, "devices.html") # Devices page connects to API seperately to allow updates without refresh.


def metricsDashboard(request: HttpRequest) -> render:
    """
    Generate and Display Metrics Dashboard.
    Using Plotly.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        render: Rendered Plotly dashboard.
    """
    generateLog('/metrics', 200, True)

    tablehtml: str = getAvailTable()

    # System Metrics Timeline
    statsDF: pd.DataFrame = pd.DataFrame(list(SystemMetric.objects.values()))
    if not statsDF.empty:
        statsDF["timestamp"] = pd.to_datetime(statsDF["timestamp"])
        sys_fig: go.Figure = px.scatter(
            statsDF,
            x="timestamp",
            y="endpoint",
            color="success",
            symbol="success",
            title="System Events Timeline",
        )
        sys_fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
        sys_html: str = sys_fig.to_html(full_html=False)
    else:
        sys_html: str = "<p>No system metrics yet</p>"

    return render(
        request,
        "metrics.html",
        {
            "table": mark_safe(tablehtml), # pass HTML table through to template.
            "system_chart": mark_safe(sys_html), # pass timeline to template.
        },
    )