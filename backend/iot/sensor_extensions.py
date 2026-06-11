from django.contrib.gis.db import models


class RiverBuoy(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    river_name = models.CharField(max_length=200)
    water_level_m = models.FloatField(default=0.0)
    alert_level_m = models.FloatField(default=3.0)
    is_active = models.BooleanField(default=True)
    last_reading_at = models.DateTimeField(null=True, blank=True)


class PestTrap(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.SET_NULL, null=True, blank=True)
    pest_count = models.PositiveIntegerField(default=0)
    last_image = models.ImageField(upload_to="pest_traps/", blank=True)
    ai_diagnosis = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
