from django.contrib import admin

from .models import MarketPrice


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ["crop_name", "market_name", "price_per_kg", "trend", "recorded_at"]
