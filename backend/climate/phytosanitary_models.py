from django.db import models


class PhytosanitaryTreatment(models.Model):
    crop_type = models.CharField(max_length=50)
    week_number = models.PositiveIntegerField(help_text="Semaine après semis")
    treatment_name = models.CharField(max_length=200)
    product = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=100, blank=True)
    target_pest = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["crop_type", "week_number"]
