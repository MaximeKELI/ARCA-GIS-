import requests
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CarbonCredit
from .serializers import CarbonCreditSerializer


class CarbonCreditListView(generics.ListAPIView):
    serializer_class = CarbonCreditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CarbonCredit.objects.filter(owner=self.request.user)


class CarbonEstimateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        parcel_id = request.data.get("parcel_id")
        area_ha = request.data.get("area_hectares", 1.0)
        crop_type = request.data.get("crop_type", "maize")
        try:
            resp = requests.post(f"{settings.AI_MODULE_URL}/carbon-estimate",
                                 json={"area_hectares": area_ha, "crop_type": crop_type}, timeout=10)
            return Response(resp.json())
        except requests.RequestException:
            co2 = area_ha * 2.5
            return Response({
                "co2_tons_year": co2, "credit_value_usd": co2 * 15,
                "methodology": "ARCA-GIS-VM001", "source": "fallback",
            })
