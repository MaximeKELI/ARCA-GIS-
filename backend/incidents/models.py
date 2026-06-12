from django.conf import settings
from django.contrib.gis.db import models


class Incident(models.Model):
    class IncidentType(models.TextChoices):
        SOS = "sos", "SOS Urgence"
        FIRE = "fire", "Incendie"
        FLOOD = "flood", "Inondation"
        DROUGHT = "drought", "Sécheresse"
        PEST_ATTACK = "pest_attack", "Attaque ravageurs"
        ACCIDENT = "accident", "Accident"
        MEDICAL = "medical", "Urgence médicale"
        OTHER = "other", "Autre"

    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        ACKNOWLEDGED = "acknowledged", "Pris en charge"
        IN_PROGRESS = "in_progress", "En cours"
        RESOLVED = "resolved", "Résolu"
        CANCELLED = "cancelled", "Annulé"

    class Priority(models.TextChoices):
        LOW = "low", "Faible"
        MEDIUM = "medium", "Moyen"
        HIGH = "high", "Élevé"
        CRITICAL = "critical", "Critique"

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reported_incidents",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_incidents",
    )
    incident_type = models.CharField(max_length=20, choices=IncidentType.choices)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.HIGH,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.PointField(srid=4326)
    address = models.CharField(max_length=300, blank=True)
    photo = models.ImageField(upload_to="incidents/", blank=True)
    people_affected = models.PositiveIntegerField(default=0)
    is_sos = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if self.incident_type == self.IncidentType.SOS:
            self.is_sos = True
            self.priority = self.Priority.CRITICAL
        super().save(*args, **kwargs)


from .ops_models import InterventionLog, RescueVolunteer  # noqa: E402, F401
