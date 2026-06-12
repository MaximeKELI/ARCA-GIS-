from django.conf import settings
from django.contrib.gis.db import models


class Cooperative(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    location = models.PointField(srid=4326, null=True, blank=True)
    president = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="led_cooperatives",
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="cooperatives", blank=True)
    member_count = models.PositiveIntegerField(default=0)
    total_hectares = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


from .v7_models import CooperativeVote, EquipmentReservation, VoteBallot  # noqa: E402, F401
