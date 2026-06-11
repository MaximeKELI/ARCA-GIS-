from django.conf import settings
from django.db import models


class Mentorship(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Actif"
        COMPLETED = "completed", "Terminé"
        PAUSED = "paused", "En pause"

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentoring"
    )
    mentee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentored_by"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    focus_crop = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["mentor", "mentee"]


class MentorshipSession(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name="sessions")
    topic = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    scheduled_at = models.DateTimeField()
    completed = models.BooleanField(default=False)
