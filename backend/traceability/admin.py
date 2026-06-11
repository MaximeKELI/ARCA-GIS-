from django.contrib import admin

from .models import HarvestRecord


@admin.register(HarvestRecord)
class HarvestRecordAdmin(admin.ModelAdmin):
    list_display = ["certificate_id", "crop_type", "quantity_kg", "farmer", "harvest_date"]
    search_fields = ["certificate_id", "blockchain_hash"]
