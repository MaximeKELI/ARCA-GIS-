from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WaterPoint, WaterQuota
from .serializers import WaterPointSerializer, WaterQuotaSerializer


class WaterPointListView(generics.ListAPIView):
    serializer_class = WaterPointSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = WaterPoint.objects.filter(is_functional=True)
    filterset_fields = ["point_type", "region"]


class WaterQuotaListView(generics.ListAPIView):
    serializer_class = WaterQuotaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WaterQuota.objects.filter(user=self.request.user)


class WaterConflictView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        low = WaterPoint.objects.filter(current_level_pct__lt=30, is_functional=True)
        return Response({
            "conflict_risk": low.count() > 0,
            "low_points": WaterPointSerializer(low[:10], many=True).data,
            "recommendation": "Réduire irrigation de 30%" if low.exists() else "Niveaux normaux",
        })
