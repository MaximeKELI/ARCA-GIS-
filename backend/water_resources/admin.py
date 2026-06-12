from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import WaterPoint, WaterQuota

admin.site.register(WaterPoint, GISModelAdmin)
admin.site.register(WaterQuota)
