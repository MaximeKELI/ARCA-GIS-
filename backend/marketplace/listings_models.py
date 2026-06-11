from django.conf import settings
from django.db import models


class CropListing(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Disponible"
        SOLD = "sold", "Vendu"
        EXPIRED = "expired", "Expiré"

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
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
