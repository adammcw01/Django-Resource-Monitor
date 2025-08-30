"""
This file defines the data models for the app.
The database for this app is left as default SQLite.
"""
from django.db import models

class DeviceStatus(models.Model):
    """
    This model stores each response from the Flask API
    """
    device_id = models.IntegerField()
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    status = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Inserted timestamp

class SystemMetric(models.Model):
    """
    This model is used to store system health metrics.
    """
    endpoint = models.CharField(max_length=200)   # The main dashboard, metrics dashboard, or the devices page.
    status_code = models.IntegerField()           # HTTP status code
    success = models.BooleanField()               # Did it succeed (2xx = True, else False)
    timestamp = models.DateTimeField(auto_now_add=True) # Inserted timestamp
