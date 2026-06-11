from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "role", "country", "is_available", "is_active"]
    list_filter = ["role", "country", "is_available", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("ARCA-GIS", {
            "fields": ("role", "phone", "organization", "country", "region",
                       "last_position", "is_available"),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("ARCA-GIS", {
            "fields": ("role", "phone", "organization", "country", "region"),
        }),
    )
