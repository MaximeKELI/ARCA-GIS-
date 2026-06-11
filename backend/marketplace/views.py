from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MarketPrice
from .serializers import MarketPriceSerializer
from .services import get_latest_prices, seed_market_prices


class MarketPriceListView(generics.ListAPIView):
    serializer_class = MarketPriceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        country = self.request.query_params.get("country")
        crop = self.request.query_params.get("crop")
        return get_latest_prices(country, crop)


class MarketSeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.user.is_admin_user:
            return Response({"error": "Admin requis"}, status=403)
        seed_market_prices()
        return Response({"status": "ok"})
