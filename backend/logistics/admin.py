from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import ShipmentRequest, Transporter

admin.site.register(Transporter)
admin.site.register(ShipmentRequest, GISModelAdmin)
