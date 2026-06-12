from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Cooperative
from .v7_models import CooperativeVote, EquipmentReservation, VoteBallot


@admin.register(Cooperative)
class CooperativeAdmin(GISModelAdmin):
    list_display = ["name", "country", "region", "member_count", "is_active"]


@admin.register(CooperativeVote)
class CooperativeVoteAdmin(admin.ModelAdmin):
    list_display = ["title", "cooperative", "is_open", "ends_at"]


@admin.register(EquipmentReservation)
class EquipmentReservationAdmin(admin.ModelAdmin):
    list_display = ["equipment_name", "cooperative", "reserved_by", "start_date", "status"]


admin.site.register(VoteBallot)
