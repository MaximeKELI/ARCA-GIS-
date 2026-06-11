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


class CropListing(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Disponible"
        SOLD = "sold", "Vendu"
        EXPIRED = "expired", "Expiré"

    seller = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="listings")
    crop_type = models.CharField(max_length=50)
    quantity_kg = models.FloatField()
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="XOF")
    quality_grade = models.CharField(max_length=10, default="A")
    harvest_certificate = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
