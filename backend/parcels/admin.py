from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Parcel


@admin.register(Parcel)
class ParcelAdmin(GISModelAdmin):
    list_display = ["name", "owner", "crop_type", "health_status", "area_hectares", "is_active"]
    list_filter = ["crop_type", "health_status", "is_active"]
    search_fields = ["name", "owner__username"]
