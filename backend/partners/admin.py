from django.contrib import admin

from .models import PartnerAPIKey


@admin.register(PartnerAPIKey)
class PartnerAPIKeyAdmin(admin.ModelAdmin):
    list_display = ["name", "partner_type", "is_active", "created_at"]
    readonly_fields = ["api_key"]
