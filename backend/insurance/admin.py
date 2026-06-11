from django.contrib import admin

from .models import InsuranceClaim, InsurancePolicy


admin.site.register(InsurancePolicy)
admin.site.register(InsuranceClaim)
