from django.conf import settings
from django.db import models


class Payment(models.Model):
    class Provider(models.TextChoices):
        ORANGE_MONEY = "orange_money", "Orange Money"
        MTN_MOMO = "mtn_momo", "MTN MoMo"
        WAVE = "wave", "Wave"
        MOOV = "moov", "Moov Money"

    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        COMPLETED = "completed", "Complété"
        FAILED = "failed", "Échoué"
        REFUNDED = "refunded", "Remboursé"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, choices=Provider.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="XOF")
    phone = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    provider_transaction_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
