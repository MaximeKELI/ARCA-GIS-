from django.conf import settings
from django.db import models


class LiveAuction(models.Model):
    class Status(models.TextChoices):
        LIVE = "live", "En cours"
        CLOSED = "closed", "Terminée"

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auctions")
    crop_type = models.CharField(max_length=50)
    quantity_kg = models.FloatField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    highest_bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="bids_won",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.LIVE)
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class GroupPurchase(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    product_type = models.CharField(max_length=50, choices=[
        ("fertilizer", "Engrais"), ("seed", "Semences"), ("pesticide", "Pesticide"),
    ])
    target_quantity_kg = models.FloatField()
    current_quantity_kg = models.FloatField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField(max_length=100)
    deadline = models.DateField()
    is_open = models.BooleanField(default=True)


class FarmerCreditScore(models.Model):
    farmer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="credit_score")
    score = models.PositiveIntegerField(default=500)
    grade = models.CharField(max_length=5, default="B")
    harvests_on_time = models.PositiveIntegerField(default=0)
    loans_repaid = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)


class ExportCertificate(models.Model):
    exporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crop_type = models.CharField(max_length=50)
    quantity_kg = models.FloatField()
    destination_country = models.CharField(max_length=100)
    phytosanitary_cert = models.CharField(max_length=100, blank=True)
    eur1_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default="pending")
    issued_at = models.DateTimeField(null=True, blank=True)


class InputPrice(models.Model):
    product = models.CharField(max_length=100)
    product_type = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default="kg")
    currency = models.CharField(max_length=10, default="XOF")
    recorded_at = models.DateTimeField(auto_now_add=True)
