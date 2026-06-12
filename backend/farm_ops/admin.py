from django.contrib import admin

from .models import BudgetEntry, CropSeason, FarmTask, FieldJournal, HarvestJournal, InputInventory

admin.site.register(CropSeason)
admin.site.register(HarvestJournal)
admin.site.register(FieldJournal)
admin.site.register(InputInventory)
admin.site.register(FarmTask)
admin.site.register(BudgetEntry)
