from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import EarlyWarningAlert, RadioHFStation, RefugeCenter

admin.site.register(RefugeCenter, GISModelAdmin)
admin.site.register(EarlyWarningAlert, GISModelAdmin)
admin.site.register(RadioHFStation, GISModelAdmin)
