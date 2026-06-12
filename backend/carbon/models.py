from django.conf import settings
from django.db import models


class CarbonCredit(models.Model):
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.CASCADE, related_name="carbon_credits")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    co2_tons_sequestered = models.FloatField(default=0.0)
    credit_value_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    methodology = models.CharField(max_length=100, default="ARCA-GIS-VM001")
    verified = models.BooleanField(default=False)
    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
