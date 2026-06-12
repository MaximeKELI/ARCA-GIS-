from django.db import models


class SeasonalChallenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    action = models.CharField(max_length=50)
    target_count = models.PositiveIntegerField(default=1)
    points_reward = models.PositiveIntegerField(default=50)
    region = models.CharField(max_length=100, blank=True)
    starts_at = models.DateField()
    ends_at = models.DateField()
    is_active = models.BooleanField(default=True)
