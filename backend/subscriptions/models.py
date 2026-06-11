from django.conf import settings
from django.db import models


class Plan(models.Model):
    class Tier(models.TextChoices):
        FREE = "free", "Gratuit"
        FARMER = "farmer", "Agriculteur Pro"
        COOP = "coop", "Coopérative"
        ENTERPRISE = "enterprise", "Entreprise"

    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=20, choices=Tier.choices, unique=True)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="XOF")
    features = models.JSONField(default=list)
    max_parcels = models.PositiveIntegerField(default=3)
    max_alerts = models.PositiveIntegerField(default=10)
    ai_analysis_limit = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    payment_reference = models.CharField(max_length=100, blank=True)
