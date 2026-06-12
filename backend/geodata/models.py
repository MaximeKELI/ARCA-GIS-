from django.conf import settings
from django.contrib.gis.db import models


class CommunityMapPoint(models.Model):
    class PointCategory(models.TextChoices):
        WELL = "well", "Puits"
        MARKET = "market", "Marché"
        ROAD = "road", "Route"
        SCHOOL = "school", "École"
        CLINIC = "clinic", "Dispensaire"
        OTHER = "other", "Autre"

    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=PointCategory.choices)
    location = models.PointField(srid=4326)
    description = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class WMSLayer(models.Model):
    name = models.CharField(max_length=200)
    source_url = models.URLField()
    layer_name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    opacity = models.FloatField(default=0.7)
