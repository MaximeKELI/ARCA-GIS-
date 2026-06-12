from django.conf import settings
from django.contrib.gis.db import models


class Transporter(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    region = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50, default="camion")
    capacity_kg = models.FloatField(default=5000)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    rating = models.FloatField(default=4.0)
    is_available = models.BooleanField(default=True)


class ShipmentRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        QUOTED = "quoted", "Devis envoyé"
        ACCEPTED = "accepted", "Accepté"
        IN_TRANSIT = "in_transit", "En transit"
        DELIVERED = "delivered", "Livré"

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shipments")
    transporter = models.ForeignKey(Transporter, on_delete=models.SET_NULL, null=True, blank=True)
    crop_type = models.CharField(max_length=50)
    quantity_kg = models.FloatField()
    origin = models.PointField(srid=4326)
    destination = models.PointField(srid=4326)
    distance_km = models.FloatField(default=0)
    quoted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
