import hashlib
import json
from django.conf import settings
from django.db import models


class HarvestRecord(models.Model):
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.CASCADE, related_name="harvests")
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crop_type = models.CharField(max_length=50)
    quantity_kg = models.FloatField()
    quality_grade = models.CharField(max_length=20, default="A")
    harvest_date = models.DateField()
    blockchain_hash = models.CharField(max_length=64, blank=True)
    previous_hash = models.CharField(max_length=64, blank=True)
    certificate_id = models.CharField(max_length=50, unique=True)
    destination = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-harvest_date"]

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            self.certificate_id = f"ARCA-{self.parcel_id}-{self.harvest_date.strftime('%Y%m%d')}"
        if not self.blockchain_hash:
            last = HarvestRecord.objects.order_by("-created_at").first()
            self.previous_hash = last.blockchain_hash if last else "0" * 64
            data = json.dumps({
                "cert": self.certificate_id,
                "parcel": self.parcel_id,
                "qty": self.quantity_kg,
                "prev": self.previous_hash,
            }, sort_keys=True)
            self.blockchain_hash = hashlib.sha256(data.encode()).hexdigest()
        super().save(*args, **kwargs)
