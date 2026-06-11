from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import DroneMission


@admin.register(DroneMission)
class DroneMissionAdmin(GISModelAdmin):
    list_display = ["mission_type", "status", "operator", "altitude_m", "created_at"]
