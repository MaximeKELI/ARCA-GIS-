from django.conf import settings
from django.db import models


class AlertRule(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alert_rules")
    name = models.CharField(max_length=200)
    metric = models.CharField(max_length=50, choices=[
        ("soil_moisture", "Humidité sol"),
        ("health_status", "Santé parcelle"),
        ("inventory", "Stock intrants"),
        ("task_overdue", "Tâche en retard"),
    ])
    operator = models.CharField(max_length=10, default="lt")
    threshold = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notif_prefs")
    climate = models.BooleanField(default=True)
    crop = models.BooleanField(default=True)
    sos = models.BooleanField(default=True)
    market = models.BooleanField(default=True)
    quiet_start = models.TimeField(null=True, blank=True)
    quiet_end = models.TimeField(null=True, blank=True)
