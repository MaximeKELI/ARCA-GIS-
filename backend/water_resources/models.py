from django.contrib.gis.db import models


class WaterPoint(models.Model):
    class PointType(models.TextChoices):
        WELL = "well", "Puits"
        BOREHOLE = "borehole", "Forage"
        DAM = "dam", "Barrage"
        RIVER = "river", "Point d'eau fluvial"
        PUMP = "pump", "Pompe"

    name = models.CharField(max_length=200)
    point_type = models.CharField(max_length=20, choices=PointType.choices)
    location = models.PointField(srid=4326)
    region = models.CharField(max_length=100)
    capacity_m3 = models.FloatField(default=0.0)
    current_level_pct = models.FloatField(default=100.0)
    is_functional = models.BooleanField(default=True)
    community_managed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class WaterQuota(models.Model):
    water_point = models.ForeignKey(WaterPoint, on_delete=models.CASCADE, related_name="quotas")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    daily_liters = models.PositiveIntegerField(default=50)
    used_today_liters = models.PositiveIntegerField(default=0)
    crop_type = models.CharField(max_length=50, blank=True)
