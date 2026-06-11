from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import IoTSensor, SensorReading
from .serializers import IoTSensorSerializer, SensorReadingSerializer


class SensorListView(generics.ListAPIView):
    queryset = IoTSensor.objects.filter(is_active=True)
    serializer_class = IoTSensorSerializer
    permission_classes = [permissions.IsAuthenticated]


class SensorReadingListView(generics.ListAPIView):
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        sensor_id = self.kwargs.get("sensor_id")
        qs = SensorReading.objects.all()
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)
        return qs[:100]


class SensorIngestView(APIView):
    """Endpoint pour capteurs IoT (Arduino, Raspberry Pi)."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        device_id = request.data.get("device_id")
        value = request.data.get("value")
        if not device_id or value is None:
            return Response({"error": "device_id et value requis"}, status=400)

        try:
            sensor = IoTSensor.objects.get(device_id=device_id, is_active=True)
        except IoTSensor.DoesNotExist:
            return Response({"error": "Capteur inconnu"}, status=404)

        reading = SensorReading.objects.create(
            sensor=sensor,
            value=float(value),
            unit=request.data.get("unit", "%"),
            recorded_at=timezone.now(),
        )
        sensor.last_seen = timezone.now()
        if "battery" in request.data:
            sensor.battery_level = float(request.data["battery"])
        sensor.save()

        if sensor.parcel and sensor.sensor_type == "soil_moisture":
            sensor.parcel.soil_moisture = float(value)
            sensor.parcel.save(update_fields=["soil_moisture"])

        return Response(SensorReadingSerializer(reading).data, status=201)
