from django.conf import settings
from django.db import models


class RescueVolunteer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="volunteer_profile")
    skills = models.JSONField(default=list)
    vehicle_type = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)
    region = models.CharField(max_length=100)


class InterventionLog(models.Model):
    incident = models.ForeignKey("incidents.Incident", on_delete=models.CASCADE, related_name="interventions")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.TextField()
    status_change = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
