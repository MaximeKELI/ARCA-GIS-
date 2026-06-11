from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Incident


@admin.register(Incident)
class IncidentAdmin(GISModelAdmin):
    list_display = ["title", "incident_type", "status", "priority", "is_sos", "reporter", "created_at"]
    list_filter = ["incident_type", "status", "priority", "is_sos"]
    search_fields = ["title", "description", "reporter__username"]
