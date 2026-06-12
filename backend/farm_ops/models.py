from django.conf import settings
from django.db import models


class CropSeason(models.Model):
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.CASCADE, related_name="seasons")
    year = models.PositiveIntegerField()
    crop_type = models.CharField(max_length=50)
    planting_date = models.DateField(null=True, blank=True)
    harvest_date = models.DateField(null=True, blank=True)
    yield_kg = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="active")

    class Meta:
        ordering = ["-year"]
        unique_together = ["parcel", "year", "crop_type"]


class HarvestJournal(models.Model):
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.CASCADE, related_name="farm_harvests")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crop_type = models.CharField(max_length=50)
    quantity_kg = models.FloatField()
    quality_grade = models.CharField(max_length=10, default="A")
    harvest_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-harvest_date"]


class FieldJournal(models.Model):
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.CASCADE, related_name="journal_entries", null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entry_date = models.DateField()
    weather_note = models.CharField(max_length=200, blank=True)
    rainfall_mm = models.FloatField(null=True, blank=True)
    observation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-entry_date"]


class InputInventory(models.Model):
    class ProductType(models.TextChoices):
        SEED = "seed", "Semences"
        FERTILIZER = "fertilizer", "Engrais"
        PESTICIDE = "pesticide", "Pesticide"
        TOOL = "tool", "Outil"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inventory")
    product_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=ProductType.choices)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, default="kg")
    alert_threshold = models.FloatField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_low(self):
        return self.quantity <= self.alert_threshold


class FarmTask(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "À faire"
        DONE = "done", "Terminé"
        SKIPPED = "skipped", "Ignoré"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farm_tasks")
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    crop_type = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    source = models.CharField(max_length=50, default="manual")
    created_at = models.DateTimeField(auto_now_add=True)


class BudgetEntry(models.Model):
    class EntryType(models.TextChoices):
        INCOME = "income", "Revenu"
        EXPENSE = "expense", "Dépense"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budget_entries")
    entry_type = models.CharField(max_length=20, choices=EntryType.choices)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="XOF")
    description = models.CharField(max_length=300, blank=True)
    entry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
