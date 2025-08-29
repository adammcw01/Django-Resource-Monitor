from django.db import models

class DeviceStatus(models.Model):
    device_id = models.IntegerField()
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    status = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)  # auto timestamp

class SystemMetric(models.Model):
    endpoint = models.CharField(max_length=200)   # e.g. "/devices", "/metrics"
    status_code = models.IntegerField()           # HTTP status code (200, 500, etc.)
    success = models.BooleanField()               # Did it succeed?
    timestamp = models.DateTimeField(auto_now_add=True)
