from django.conf import settings
from django.db import models


class InsurancePolicy(models.Model):
    class PolicyType(models.TextChoices):
        DROUGHT = "drought", "Sécheresse"
        FLOOD = "flood", "Inondation"
        CROP_FAILURE = "crop_failure", "Échec récolte"

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="policies")
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.CASCADE)
    policy_type = models.CharField(max_length=20, choices=PolicyType.choices)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    trigger_threshold = models.JSONField(default=dict)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InsuranceClaim(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        TRIGGERED = "triggered", "Déclenché"
        PAID = "paid", "Payé"
        REJECTED = "rejected", "Rejeté"

    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE, related_name="claims")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    trigger_data = models.JSONField(default=dict)
    payout_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
