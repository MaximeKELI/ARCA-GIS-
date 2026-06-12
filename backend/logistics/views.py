from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShipmentRequest, Transporter
from .serializers import ShipmentRequestSerializer, TransporterSerializer


class TransporterListView(generics.ListAPIView):
    serializer_class = TransporterSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transporter.objects.filter(is_available=True)
    filterset_fields = ["region"]


class ShipmentListCreateView(generics.ListCreateAPIView):
    serializer_class = ShipmentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShipmentRequest.objects.filter(farmer=self.request.user)


class ShipmentQuoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            shipment = ShipmentRequest.objects.get(pk=pk, farmer=request.user)
        except ShipmentRequest.DoesNotExist:
            return Response({"error": "Expédition introuvable"}, status=404)
        distance = float(request.data.get("distance_km", shipment.distance_km or 50))
        transporter = Transporter.objects.filter(is_available=True, region=request.user.region).first()
        if transporter:
            price = distance * float(transporter.price_per_km)
            shipment.transporter = transporter
            shipment.distance_km = distance
            shipment.quoted_price = price
            shipment.status = ShipmentRequest.Status.QUOTED
            shipment.save()
        return Response(ShipmentRequestSerializer(shipment).data)
