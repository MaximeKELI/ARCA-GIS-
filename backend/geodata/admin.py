from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import CommunityMapPoint, WMSLayer

admin.site.register(CommunityMapPoint, GISModelAdmin)
admin.site.register(WMSLayer)
