from django.contrib.gis.db import models


class LoRaDevice(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    device_type = models.CharField(max_length=50)
    network = models.CharField(max_length=20, default="lorawan")
    last_payload = models.JSONField(default=dict, blank=True)
    firmware_version = models.CharField(max_length=20, default="1.0.0")
    is_active = models.BooleanField(default=True)


class SoilStation(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    ph = models.FloatField(null=True, blank=True)
    nitrogen = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    conductivity = models.FloatField(null=True, blank=True)
    last_reading_at = models.DateTimeField(null=True, blank=True)


class RainGauge(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    rainfall_mm_today = models.FloatField(default=0)
    alert_threshold_mm = models.FloatField(default=50)


class LivestockCollar(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    herd = models.ForeignKey("livestock.Herd", on_delete=models.CASCADE, related_name="collars")
    animal_id = models.CharField(max_length=50)
    location = models.PointField(srid=4326, null=True, blank=True)
    battery_pct = models.FloatField(default=100)
    is_in_geofence = models.BooleanField(default=True)
