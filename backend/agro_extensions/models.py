from django.conf import settings
from django.contrib.gis.db import models


class BeeHive(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hives")
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    colony_strength = models.CharField(max_length=20, default="medium")
    honey_production_kg = models.FloatField(default=0.0)
    last_inspection = models.DateField(null=True, blank=True)
    swarm_alert = models.BooleanField(default=False)


class FishPond(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ponds")
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    area_m2 = models.FloatField(default=100)
    fish_species = models.CharField(max_length=100, default="tilapia")
    stock_count = models.PositiveIntegerField(default=0)
    water_quality = models.CharField(max_length=20, default="good")
    mortality_rate = models.FloatField(default=0.0)


class AgroforestryPlot(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    geometry = models.PolygonField(srid=4326)
    tree_species = models.JSONField(default=list)
    crop_association = models.CharField(max_length=100, blank=True)
    tree_count = models.PositiveIntegerField(default=0)
    carbon_bonus = models.FloatField(default=0.0)


class SeedBankEntry(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crop_type = models.CharField(max_length=50)
    variety = models.CharField(max_length=100)
    quantity_kg = models.FloatField()
    region = models.CharField(max_length=100)
    harvest_year = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)


class CompostBatch(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326, null=True, blank=True)
    input_materials = models.JSONField(default=list)
    volume_m3 = models.FloatField(default=1.0)
    maturity_pct = models.PositiveIntegerField(default=0)
    ready_date = models.DateField(null=True, blank=True)
