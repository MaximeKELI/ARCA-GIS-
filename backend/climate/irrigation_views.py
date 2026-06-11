import requests
from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class IrrigationAdviceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        crop_type = request.data.get("crop_type", "maize")
        soil_moisture = request.data.get("soil_moisture", 50)

        try:
            resp = requests.post(
                f"{settings.AI_MODULE_URL}/irrigation",
                json={"lat": lat, "lng": lng, "crop_type": crop_type, "soil_moisture": soil_moisture},
                timeout=10,
            )
            return Response(resp.json())
        except requests.RequestException:
            should_irrigate = soil_moisture < 40
            return Response({
                "should_irrigate": should_irrigate,
                "amount_mm": 25 if should_irrigate else 0,
                "best_time": "05:00-07:00",
                "frequency": "tous les 2 jours" if should_irrigate else "non nécessaire",
                "source": "fallback",
            })
