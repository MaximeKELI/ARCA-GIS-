from django.db import models


class CropCalendar(models.Model):
    crop_type = models.CharField(max_length=50)
    crop_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Côte d'Ivoire")
    planting_start = models.CharField(max_length=20, help_text="MM-DD")
    planting_end = models.CharField(max_length=20)
    harvest_start = models.CharField(max_length=20)
    harvest_end = models.CharField(max_length=20)
    treatments = models.JSONField(default=list)
    tips = models.TextField(blank=True)

    class Meta:
        ordering = ["crop_type", "region"]
        unique_together = ["crop_type", "region"]
