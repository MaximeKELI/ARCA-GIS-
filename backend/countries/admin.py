from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import CountryConfig

admin.site.register(CountryConfig, GISModelAdmin)
