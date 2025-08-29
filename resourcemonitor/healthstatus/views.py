from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import requests
import logging

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# --- Logging setup ---
logger = logging.getLogger(__name__)

# --- Prometheus metrics ---
DEVICE_REQUESTS = Counter("device_requests_total", "Total requests to fetch devices")
DEVICE_ERRORS = Counter("device_errors_total", "Total errors fetching devices")

DEVICE_API_URL = "http://127.0.0.1:8000/devices"

def callDeviceService(request):
    """Fetch devices from a mock API and return as JSON"""
    try:
        DEVICE_REQUESTS.inc()
        resp = requests.get(DEVICE_API_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        logger.info("Fetched device data: %s", data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        DEVICE_ERRORS.inc()
        logger.error("Error fetching device data: %s", e)
        return JsonResponse({"error": str(e)}, status=500)

def frontEnd(request):
#    try:
#        resp = requests.get(DEVICE_API_URL, timeout=5)
#        resp.raise_for_status()
#        data = resp.json()
#    except Exception as e:
#        data = []
#        logger.error("Error rendering devices page: %s", e)
#    return render(request, "devices.html", {"devices": data})
    return render(request, "devices.html")


def metrics(request):
    """Prometheus scrape endpoint"""
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)