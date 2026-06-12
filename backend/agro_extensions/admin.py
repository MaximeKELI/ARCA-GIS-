from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import AgroforestryPlot, BeeHive, CompostBatch, FishPond, SeedBankEntry

admin.site.register(BeeHive, GISModelAdmin)
admin.site.register(FishPond, GISModelAdmin)
admin.site.register(AgroforestryPlot, GISModelAdmin)
admin.site.register(SeedBankEntry)
admin.site.register(CompostBatch, GISModelAdmin)
