from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Plan, UserSubscription
from .serializers import PlanSerializer, UserSubscriptionSerializer


class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]


class MySubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            sub = UserSubscription.objects.get(user=request.user)
            return Response(UserSubscriptionSerializer(sub).data)
        except UserSubscription.DoesNotExist:
            free_plan, _ = Plan.objects.get_or_create(
                tier=Plan.Tier.FREE,
                defaults={"name": "Gratuit", "features": ["3 parcelles", "5 analyses IA/mois"]},
            )
            sub = UserSubscription.objects.create(user=request.user, plan=free_plan)
            return Response(UserSubscriptionSerializer(sub).data)
