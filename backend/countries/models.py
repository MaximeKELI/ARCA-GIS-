from django.contrib.gis.db import models


class CountryConfig(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=10, default="XOF")
    timezone = models.CharField(max_length=50, default="Africa/Abidjan")
    default_language = models.CharField(max_length=5, default="fr")
    emergency_number = models.CharField(max_length=20, default="180")
    bounds = models.PolygonField(srid=4326, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    settings = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "country configs"

    def __str__(self):
        return self.name
