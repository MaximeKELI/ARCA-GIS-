from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ("planting", "Semis"), ("irrigation", "Irrigation"),
        ("pest", "Ravageurs"), ("harvest", "Récolte"), ("climate", "Climat"),
    ])
    language = models.CharField(max_length=5, default="fr")
    video_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=10)
    crop_types = models.JSONField(default=list)
    difficulty = models.CharField(max_length=20, default="beginner")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]


class CourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    progress_pct = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "course"]
