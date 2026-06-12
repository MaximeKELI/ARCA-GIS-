from django.conf import settings
from django.contrib.gis.db import models


class Parcel(models.Model):
    class CropType(models.TextChoices):
        MAIZE = "maize", "Maïs"
        RICE = "rice", "Riz"
        CASSAVA = "cassava", "Manioc"
        COCOA = "cocoa", "Cacao"
        COFFEE = "coffee", "Café"
        COTTON = "cotton", "Coton"
        GROUNDNUT = "groundnut", "Arachide"
        OTHER = "other", "Autre"

    class HealthStatus(models.TextChoices):
        EXCELLENT = "excellent", "Excellent"
        GOOD = "good", "Bon"
        MODERATE = "moderate", "Modéré"
        POOR = "poor", "Mauvais"
        CRITICAL = "critical", "Critique"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parcels",
    )
    name = models.CharField(max_length=200)
    crop_type = models.CharField(max_length=20, choices=CropType.choices)
    geometry = models.PolygonField(srid=4326)
    area_hectares = models.FloatField(default=0.0)
    health_status = models.CharField(
        max_length=20,
        choices=HealthStatus.choices,
        default=HealthStatus.GOOD,
    )
    soil_moisture = models.FloatField(default=50.0, help_text="Pourcentage 0-100")
    planting_date = models.DateField(null=True, blank=True)
    expected_harvest = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_crop_type_display()})"

    def save(self, *args, **kwargs):
        if self.geometry and not self.area_hectares:
            self.area_hectares = round(self.geometry.area * 111320 * 111320 / 10000, 2)
        super().save(*args, **kwargs)


from .history_models import ParcelChangeLog  # noqa: E402, F401
