from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .history_models import ParcelChangeLog
from .models import Parcel


@admin.register(Parcel)
class ParcelAdmin(GISModelAdmin):
    list_display = ["name", "owner", "crop_type", "health_status", "area_hectares", "is_active"]
    list_filter = ["crop_type", "health_status", "is_active"]
    search_fields = ["name", "owner__username"]


@admin.register(ParcelChangeLog)
class ParcelChangeLogAdmin(admin.ModelAdmin):
    list_display = ["parcel", "field_name", "changed_by", "changed_at"]
    list_filter = ["field_name"]
