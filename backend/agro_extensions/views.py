import requests
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AgroforestryPlot, BeeHive, CompostBatch, FishPond, SeedBankEntry
from .serializers import (
    AgroforestryPlotSerializer, BeeHiveSerializer, CompostBatchSerializer,
    FishPondSerializer, SeedBankEntrySerializer,
)


class BeeHiveListCreateView(generics.ListCreateAPIView):
    serializer_class = BeeHiveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        return BeeHive.objects.all() if u.is_admin_user else BeeHive.objects.filter(owner=u)


class FishPondListCreateView(generics.ListCreateAPIView):
    serializer_class = FishPondSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        return FishPond.objects.all() if u.is_admin_user else FishPond.objects.filter(owner=u)


class AgroforestryListCreateView(generics.ListCreateAPIView):
    serializer_class = AgroforestryPlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        return AgroforestryPlot.objects.all() if u.is_admin_user else AgroforestryPlot.objects.filter(owner=u)


class SeedBankListCreateView(generics.ListCreateAPIView):
    serializer_class = SeedBankEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SeedBankEntry.objects.filter(is_available=True)


class CompostListCreateView(generics.ListCreateAPIView):
    serializer_class = CompostBatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompostBatch.objects.filter(owner=self.request.user)


class CropRotationPlanView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            resp = requests.post(f"{settings.AI_MODULE_URL}/crop-rotation", json=request.data, timeout=10)
            return Response(resp.json())
        except requests.RequestException:
            return Response({
                "parcel_id": request.data.get("parcel_id"),
                "plan_years": [
                    {"year": 1, "crop": "maize", "reason": "Restauration azote"},
                    {"year": 2, "crop": "cowpea", "reason": "Fixation N"},
                    {"year": 3, "crop": "maize", "reason": "Rendement optimal"},
                ],
                "source": "fallback",
            })
