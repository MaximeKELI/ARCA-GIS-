import hashlib

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Parcel


class ParcelQRView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            parcel = Parcel.objects.get(pk=pk, owner=request.user)
        except Parcel.DoesNotExist:
            return Response({"error": "Parcelle introuvable"}, status=404)
        code = hashlib.md5(f"ARCA-{parcel.id}-{parcel.owner_id}".encode()).hexdigest()[:12].upper()
        return Response({
            "parcel_id": parcel.id, "qr_code": f"ARCA-{code}",
            "name": parcel.name, "crop": parcel.crop_type,
        })


class ParcelQRVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, code):
        for p in Parcel.objects.filter(is_active=True):
            expected = hashlib.md5(f"ARCA-{p.id}-{p.owner_id}".encode()).hexdigest()[:12].upper()
            if f"ARCA-{expected}" == code:
                return Response({"valid": True, "parcel": p.name, "crop": p.crop_type, "owner": p.owner.get_full_name()})
        return Response({"valid": False}, status=404)
