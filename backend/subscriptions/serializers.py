from rest_framework import serializers

from .models import Plan, UserSubscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "tier", "price_monthly", "currency", "features",
                  "max_parcels", "max_alerts", "ai_analysis_limit"]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan_detail = PlanSerializer(source="plan", read_only=True)

    class Meta:
        model = UserSubscription
        fields = ["id", "plan", "plan_detail", "started_at", "expires_at", "is_active"]
