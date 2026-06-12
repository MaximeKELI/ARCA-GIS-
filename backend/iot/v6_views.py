from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .v6_models import LivestockCollar, LoRaDevice, RainGauge, SoilStation


class LoRaIngestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        device_id = request.data.get("device_id")
        try:
            dev = LoRaDevice.objects.get(device_id=device_id)
        except LoRaDevice.DoesNotExist:
            return Response({"error": "Device inconnu"}, status=404)
        dev.last_payload = request.data
        dev.save()
        return Response({"status": "ok"})


class SoilStationIngestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        device_id = request.data.get("device_id")
        try:
            st = SoilStation.objects.get(device_id=device_id)
        except SoilStation.DoesNotExist:
            return Response({"error": "Station inconnue"}, status=404)
        st.ph = request.data.get("ph", st.ph)
        st.nitrogen = request.data.get("nitrogen", st.nitrogen)
        st.phosphorus = request.data.get("phosphorus", st.phosphorus)
        st.potassium = request.data.get("potassium", st.potassium)
        st.conductivity = request.data.get("conductivity", st.conductivity)
        st.last_reading_at = timezone.now()
        st.save()
        return Response({"status": "ok", "npk": {"n": st.nitrogen, "p": st.phosphorus, "k": st.potassium}})


class RainGaugeIngestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        device_id = request.data.get("device_id")
        mm = float(request.data.get("rainfall_mm", 0))
        try:
            gauge = RainGauge.objects.get(device_id=device_id)
        except RainGauge.DoesNotExist:
            return Response({"error": "Pluviomètre inconnu"}, status=404)
        gauge.rainfall_mm_today = mm
        gauge.save()
        alert = mm >= gauge.alert_threshold_mm
        return Response({"status": "ok", "mm": mm, "alert": alert})


class OTAFirmwareView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        device_id = request.data.get("device_id")
        version = request.data.get("version", "2.0.0")
        try:
            dev = LoRaDevice.objects.get(device_id=device_id)
        except LoRaDevice.DoesNotExist:
            return Response({"error": "Device inconnu"}, status=404)
        dev.firmware_version = version
        dev.save()
        return Response({"status": "ota_scheduled", "version": version, "url": f"/firmware/{version}.bin"})


class EdgeAIIngestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        return Response({
            "device_id": request.data.get("device_id"),
            "diagnosis": request.data.get("diagnosis", {"pest": "none", "confidence": 0.9}),
            "processed_on_device": True,
        })
