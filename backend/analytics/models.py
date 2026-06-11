from django.conf import settings
from django.db import models


class AnalyticsSnapshot(models.Model):
    class SnapshotType(models.TextChoices):
        DAILY = "daily", "Quotidien"
        WEEKLY = "weekly", "Hebdomadaire"
        MONTHLY = "monthly", "Mensuel"

    snapshot_type = models.CharField(max_length=20, choices=SnapshotType.choices)
    region = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="Côte d'Ivoire")
    data = models.JSONField(default=dict)
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]


class CropHistory(models.Model):
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.CASCADE, related_name="history")
    health_status = models.CharField(max_length=20)
    soil_moisture = models.FloatField()
    temperature = models.FloatField(null=True, blank=True)
    rainfall_mm = models.FloatField(null=True, blank=True)
    ndvi_score = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField()

    class Meta:
        ordering = ["-recorded_at"]
