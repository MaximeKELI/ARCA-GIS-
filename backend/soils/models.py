from django.contrib.gis.db import models


class SoilZone(models.Model):
    class SoilType(models.TextChoices):
        FERRALSOL = "ferralsol", "Ferralsol (latérite)"
        LEPTOSOL = "leptosol", "Leptosol (rocheux)"
        VERTISOL = "vertisol", "Vertisol (argileux)"
        CAMBISOL = "cambisol", "Cambisol"
        FLUVISOL = "fluvisol", "Fluvisol (alluvial)"
        ARENOSOL = "arenosol", "Arenosol (sableux)"

    name = models.CharField(max_length=200)
    soil_type = models.CharField(max_length=20, choices=SoilType.choices)
    geometry = models.PolygonField(srid=4326)
    ph = models.FloatField(null=True, blank=True)
    organic_matter = models.FloatField(null=True, blank=True, help_text="%")
    texture = models.CharField(max_length=50, blank=True)
    suitability = models.JSONField(default=dict, blank=True)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, default="FAO/ISRIC")

    class Meta:
        ordering = ["name"]
