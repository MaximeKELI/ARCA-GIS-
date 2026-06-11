from django.db import models


class MarketPrice(models.Model):
    crop_type = models.CharField(max_length=50)
    crop_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    market_name = models.CharField(max_length=200)
    price_per_kg = models.FloatField(help_text="Prix en FCFA/kg")
    currency = models.CharField(max_length=10, default="XOF")
    trend = models.CharField(max_length=10, choices=[
        ("up", "Hausse"), ("down", "Baisse"), ("stable", "Stable"),
    ], default="stable")
    recorded_at = models.DateTimeField()
    source = models.CharField(max_length=100, default="ARCA-GIS")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]
