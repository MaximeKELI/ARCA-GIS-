from rest_framework import serializers

from .models import InsuranceClaim, InsurancePolicy


class InsurancePolicySerializer(serializers.ModelSerializer):
    policy_type_display = serializers.CharField(source="get_policy_type_display", read_only=True)

    class Meta:
        model = InsurancePolicy
        fields = [
            "id", "parcel", "policy_type", "policy_type_display",
            "coverage_amount", "premium", "trigger_threshold",
            "start_date", "end_date", "is_active", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        validated_data["farmer"] = self.context["request"].user
        return super().create(validated_data)


class InsuranceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = ["id", "policy", "status", "trigger_data", "payout_amount", "triggered_at", "created_at"]
