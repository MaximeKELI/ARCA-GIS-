from django.conf import settings
from django.db import models


class Badge(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="star")
    points = models.PositiveIntegerField(default=10)
    criteria = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gamification")
    total_points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    badges = models.ManyToManyField(Badge, blank=True, related_name="earners")
    streak_days = models.PositiveIntegerField(default=0)

    def add_points(self, pts: int):
        self.total_points += pts
        self.level = 1 + self.total_points // 100
        self.save()


class PointEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="point_events")
    action = models.CharField(max_length=50)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


from .challenge_models import SeasonalChallenge  # noqa: E402, F401
