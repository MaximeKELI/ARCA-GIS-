from rest_framework import serializers

from .models import AgroforestryPlot, BeeHive, CompostBatch, FishPond, SeedBankEntry


class BeeHiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeeHive
        fields = "__all__"
        read_only_fields = ["id", "owner"]

    def create(self, v):
        v["owner"] = self.context["request"].user
        return super().create(v)


class FishPondSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishPond
        fields = "__all__"
        read_only_fields = ["id", "owner"]

    def create(self, v):
        v["owner"] = self.context["request"].user
        return super().create(v)


class AgroforestryPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgroforestryPlot
        fields = "__all__"
        read_only_fields = ["id", "owner"]

    def create(self, v):
        v["owner"] = self.context["request"].user
        return super().create(v)


class SeedBankEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeedBankEntry
        fields = "__all__"
        read_only_fields = ["id", "contributor"]

    def create(self, v):
        v["contributor"] = self.context["request"].user
        return super().create(v)


class CompostBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompostBatch
        fields = "__all__"
        read_only_fields = ["id", "owner"]

    def create(self, v):
        v["owner"] = self.context["request"].user
        return super().create(v)
