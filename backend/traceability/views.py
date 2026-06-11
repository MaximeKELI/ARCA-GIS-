from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HarvestRecord
from .serializers import HarvestRecordSerializer


class HarvestListCreateView(generics.ListCreateAPIView):
    serializer_class = HarvestRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return HarvestRecord.objects.all()
        return HarvestRecord.objects.filter(farmer=user)


class VerifyCertificateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, cert_id):
        try:
            record = HarvestRecord.objects.get(certificate_id=cert_id)
        except HarvestRecord.DoesNotExist:
            return Response({"valid": False, "error": "Certificat introuvable"}, status=404)
        return Response({
            "valid": True,
            "certificate_id": record.certificate_id,
            "blockchain_hash": record.blockchain_hash,
            "crop_type": record.crop_type,
            "quantity_kg": record.quantity_kg,
            "harvest_date": record.harvest_date,
            "parcel": record.parcel.name,
            "farmer": record.farmer.get_full_name(),
        })
