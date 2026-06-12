import requests
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .contracts_models import BuyerContract
from .serializers import MarketPriceSerializer
from .models import MarketPrice


class BuyerContractListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BuyerContract.objects.filter(status=BuyerContract.Status.OPEN)

    def list(self, request, *args, **kwargs):
        data = [{
            "id": c.id, "crop_type": c.crop_type, "quantity_kg": c.quantity_kg,
            "max_price_per_kg": float(c.max_price_per_kg), "region": c.region,
        } for c in self.get_queryset()]
        return Response(data)

    def create(self, request, *args, **kwargs):
        c = BuyerContract.objects.create(
            buyer=request.user,
            crop_type=request.data.get("crop_type"),
            quantity_kg=request.data.get("quantity_kg"),
            max_price_per_kg=request.data.get("max_price_per_kg"),
            region=request.data.get("region", request.user.region),
        )
        return Response({"id": c.id, "status": "open"}, status=201)


class PriceForecastView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        crop = request.query_params.get("crop", "maize")
        try:
            resp = requests.post(f"{settings.AI_MODULE_URL}/price-forecast",
                                 json={"crop_type": crop}, timeout=10)
            return Response(resp.json())
        except requests.RequestException:
            latest = MarketPrice.objects.filter(crop_type=crop).first()
            return Response({
                "crop_type": crop,
                "current_price": latest.price_per_kg if latest else 250,
                "forecast_7d": "stable",
                "recommendation": "Vendre dans 2 semaines",
                "source": "fallback",
            })
