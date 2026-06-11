from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import SoilZone


@admin.register(SoilZone)
class SoilZoneAdmin(GISModelAdmin):
    list_display = ["name", "soil_type", "country", "region"]
