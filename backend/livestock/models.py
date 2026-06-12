from django.conf import settings
from django.contrib.gis.db import models


class Herd(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="herds")
    name = models.CharField(max_length=200)
    animal_type = models.CharField(max_length=50, choices=[
        ("cattle", "Bovins"), ("goat", "Caprins"), ("sheep", "Ovins"),
        ("poultry", "Volaille"), ("pig", "Porcins"),
    ])
    count = models.PositiveIntegerField(default=0)
    location = models.PointField(srid=4326, null=True, blank=True)
    pasture_area_ha = models.FloatField(default=0.0)
    health_status = models.CharField(max_length=20, default="good")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]


class VeterinaryAlert(models.Model):
    class Severity(models.TextChoices):
        LOW = "low", "Faible"
        MEDIUM = "medium", "Moyen"
        HIGH = "high", "Élevé"
        CRITICAL = "critical", "Critique"

    herd = models.ForeignKey(Herd, on_delete=models.CASCADE, related_name="alerts", null=True, blank=True)
    disease = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=Severity.choices)
    region = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    reported_at = models.DateTimeField(auto_now_add=True)
