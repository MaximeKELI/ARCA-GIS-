from django.conf import settings
from django.db import models


class VillageWhatsAppGroup(models.Model):
    village_name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    group_id = models.CharField(max_length=100, blank=True)
    admin_phone = models.CharField(max_length=20)
    member_count = models.PositiveIntegerField(default=0)
    alerts_enabled = models.BooleanField(default=True)


class WomenFarmerProgram(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="women_programs")
    cooperative = models.CharField(max_length=200, blank=True)
    training_completed = models.JSONField(default=list)
    hectares_managed = models.FloatField(default=0)
    income_xof = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    joined_at = models.DateTimeField(auto_now_add=True)


class NutritionRecord(models.Model):
    child_name = models.CharField(max_length=200)
    age_months = models.PositiveIntegerField()
    region = models.CharField(max_length=100)
    malnutrition_risk = models.CharField(max_length=20, default="low")
    food_sources = models.JSONField(default=list)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recorded_at = models.DateTimeField(auto_now_add=True)
