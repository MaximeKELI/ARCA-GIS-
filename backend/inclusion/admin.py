from django.contrib import admin

from .models import NutritionRecord, VillageWhatsAppGroup, WomenFarmerProgram

admin.site.register(VillageWhatsAppGroup)
admin.site.register(WomenFarmerProgram)
admin.site.register(NutritionRecord)
