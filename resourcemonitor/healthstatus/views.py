from django.shortcuts import render
from django.http import JsonResponse
import requests
import logging
from healthstatus.models import DeviceStatus, SystemMetric
import plotly.express as px
import pandas as pd
from .utils import generateLog, getDeviceAvail, getAvailTable
import plotly.graph_objects as go
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

DEVICE_API_URL = "http://127.0.0.1:8000/devices"

def callDeviceService(request):
    """Fetch devices from a mock API and record response in SQLite."""
    try:
        resp = requests.get(DEVICE_API_URL, timeout=5)
        resp.raise_for_status()
        devices = resp.json()
    
        for d in devices:
            DeviceStatus.objects.create(
                device_id=d["id"],
                name=d["name"],
                ip_address=d["ip_address"],
                status=d["status"],
            )

        generateLog("/devices", resp.status_code, True)

        logger.info("Stored %d device records", len(devices))
        return JsonResponse(devices, safe=False)

    except Exception as e:
        logger.error("Error fetching device data: %s", e)
        generateLog("/devices", getattr(e.response, 'status_code', 500), False) 
        return JsonResponse({"error": str(e)}, status=500)


def frontEnd(request):
    """
    Serve the front end to the client.
    """
    generateLog("/index", 200, True)
    return render(request, "devices.html")


def metricsDashboard(request):
    """Display metrics dashboard using Plotly."""
    generateLog('/metrics', 200, True)

    df = getDeviceAvail()

    # --- Device Table ---
    tablehtml = getAvailTable()

    # --- System Metrics Timeline ---
    sys_df = pd.DataFrame(list(SystemMetric.objects.values()))
    if not sys_df.empty:
        sys_df["timestamp"] = pd.to_datetime(sys_df["timestamp"])
        sys_fig = px.scatter(
            sys_df,
            x="timestamp",
            y="endpoint",
            color="success",
            symbol="success",
            title="System Events Timeline",
        )
        sys_fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
        sys_html = sys_fig.to_html(full_html=False)
    else:
        sys_html = "<p>No system metrics yet</p>"

    return render(
        request,
        "metrics.html",
        {
            "table": mark_safe(tablehtml),
            "system_chart": mark_safe(sys_html),
        },
    )