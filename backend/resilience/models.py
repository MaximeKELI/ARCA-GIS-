from django.contrib.gis.db import models


class RefugeCenter(models.Model):
    name = models.CharField(max_length=200)
    center_type = models.CharField(max_length=50, choices=[
        ("school", "École"), ("community", "Centre communautaire"),
        ("church", "Église/Mosquée"), ("hospital", "Hôpital"),
    ])
    location = models.PointField(srid=4326)
    region = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)
    contact_phone = models.CharField(max_length=20, blank=True)


class EarlyWarningAlert(models.Model):
    class AlertLevel(models.TextChoices):
        WATCH = "watch", "Surveillance"
        WARNING = "warning", "Alerte"
        EMERGENCY = "emergency", "Urgence"

    hazard_type = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=AlertLevel.choices)
    region = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    description = models.TextField()
    forecast_days = models.PositiveIntegerField(default=30)
    geometry = models.PolygonField(srid=4326, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    issued_at = models.DateTimeField(auto_now_add=True)


class RadioHFStation(models.Model):
    name = models.CharField(max_length=200)
    frequency = models.CharField(max_length=20)
    region = models.CharField(max_length=100)
    location = models.PointField(srid=4326, null=True, blank=True)
    is_operational = models.BooleanField(default=True)
