from rest_framework import serializers

from .models import BudgetEntry, CropSeason, FarmTask, FieldJournal, HarvestJournal, InputInventory


class CropSeasonSerializer(serializers.ModelSerializer):
    parcel_name = serializers.CharField(source="parcel.name", read_only=True)

    class Meta:
        model = CropSeason
        fields = "__all__"
        read_only_fields = ["id"]


class HarvestJournalSerializer(serializers.ModelSerializer):
    parcel_name = serializers.CharField(source="parcel.name", read_only=True)

    class Meta:
        model = HarvestJournal
        fields = "__all__"
        read_only_fields = ["id", "owner", "created_at"]

    def create(self, v):
        v["owner"] = self.context["request"].user
        return super().create(v)


class FieldJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldJournal
        fields = "__all__"
        read_only_fields = ["id", "author", "created_at"]

    def create(self, v):
        v["author"] = self.context["request"].user
        return super().create(v)


class InputInventorySerializer(serializers.ModelSerializer):
    is_low = serializers.BooleanField(read_only=True)

    class Meta:
        model = InputInventory
        fields = "__all__"
        read_only_fields = ["id", "owner", "created_at"]

    def create(self, v):
        v["owner"] = self.context["request"].user
        return super().create(v)


class FarmTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmTask
        fields = "__all__"
        read_only_fields = ["id", "owner", "created_at"]

    def create(self, v):
        v["owner"] = self.context["request"].user
        return super().create(v)


class BudgetEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetEntry
        fields = "__all__"
        read_only_fields = ["id", "owner", "created_at"]

    def create(self, v):
        v["owner"] = self.context["request"].user
        return super().create(v)
