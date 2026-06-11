from django.conf import settings
from django.contrib.gis.db import models


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=100, blank=True)
    resource_id = models.CharField(max_length=50, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class GeofenceZone(models.Model):
    class ZoneType(models.TextChoices):
        RISK = "risk", "Zone à risque"
        SAFE = "safe", "Zone sûre"
        FARM = "farm", "Zone agricole"
        EMERGENCY = "emergency", "Zone urgence"

    name = models.CharField(max_length=200)
    zone_type = models.CharField(max_length=20, choices=ZoneType.choices)
    geometry = models.PolygonField(srid=4326)
    description = models.TextField(blank=True)
    alert_on_enter = models.BooleanField(default=True)
    alert_on_exit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class OfflineSyncQueue(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)
    payload = models.JSONField()
    synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
