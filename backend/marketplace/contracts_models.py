from django.conf import settings
from django.db import models


class BuyerContract(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Ouvert"
        MATCHED = "matched", "Attribué"
        CLOSED = "closed", "Fermé"

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buyer_contracts")
    crop_type = models.CharField(max_length=50)
    quantity_kg = models.FloatField()
    max_price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="XOF")
    region = models.CharField(max_length=100)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
