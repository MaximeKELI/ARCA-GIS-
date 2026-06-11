from django.conf import settings
from django.db import models


class Alert(models.Model):
    class AlertType(models.TextChoices):
        CLIMATE = "climate", "Alerte climatique"
        SOS = "sos", "SOS Urgence"
        INCIDENT = "incident", "Incident"
        CROP = "crop", "Santé des cultures"
        SYSTEM = "system", "Système"

    class Severity(models.TextChoices):
        INFO = "info", "Information"
        LOW = "low", "Faible"
        MEDIUM = "medium", "Moyen"
        HIGH = "high", "Élevé"
        CRITICAL = "critical", "Critique"

    alert_type = models.CharField(max_length=20, choices=AlertType.choices)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MEDIUM)
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    target_role = models.CharField(max_length=20, blank=True)
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="alerts",
    )
    is_read = models.BooleanField(default=False)
    is_broadcast = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_severity_display()})"
