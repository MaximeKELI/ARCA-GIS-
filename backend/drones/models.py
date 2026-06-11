from django.conf import settings
from django.contrib.gis.db import models


class DroneMission(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planifié"
        IN_FLIGHT = "in_flight", "En vol"
        COMPLETED = "completed", "Terminé"
        CANCELLED = "cancelled", "Annulé"

    class MissionType(models.TextChoices):
        MAPPING = "mapping", "Cartographie"
        SPRAYING = "spraying", "Pulvérisation"
        SURVEILLANCE = "surveillance", "Surveillance"
        NDVI = "ndvi", "Analyse NDVI"

    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.SET_NULL, null=True, blank=True)
    mission_type = models.CharField(max_length=20, choices=MissionType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    flight_path = models.LineStringField(srid=4326, null=True, blank=True)
    coverage_area = models.PolygonField(srid=4326, null=True, blank=True)
    altitude_m = models.FloatField(default=50.0)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
