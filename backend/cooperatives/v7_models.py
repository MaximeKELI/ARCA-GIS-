from django.conf import settings
from django.db import models


class CooperativeVote(models.Model):
    cooperative = models.ForeignKey("cooperatives.Cooperative", on_delete=models.CASCADE, related_name="votes")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ends_at = models.DateTimeField()
    is_open = models.BooleanField(default=True)


class VoteBallot(models.Model):
    vote = models.ForeignKey(CooperativeVote, on_delete=models.CASCADE, related_name="ballots")
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice = models.CharField(max_length=100)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["vote", "voter"]


class EquipmentReservation(models.Model):
    cooperative = models.ForeignKey("cooperatives.Cooperative", on_delete=models.CASCADE, related_name="equipment")
    equipment_name = models.CharField(max_length=200)
    reserved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default="pending")
