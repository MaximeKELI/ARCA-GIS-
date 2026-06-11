from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Cooperative


@admin.register(Cooperative)
class CooperativeAdmin(GISModelAdmin):
    list_display = ["name", "country", "region", "member_count", "is_active"]
