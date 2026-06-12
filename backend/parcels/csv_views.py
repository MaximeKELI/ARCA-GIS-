import csv
from io import StringIO

from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView

from .models import Parcel


class ParcelCSVExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "name", "crop_type", "health_status", "area_ha", "soil_moisture", "region"])
        for p in Parcel.objects.filter(owner=request.user, is_active=True):
            writer.writerow([
                p.id, p.name, p.crop_type, p.health_status,
                p.area_hectares, p.soil_moisture, p.region,
            ])
        response = HttpResponse(output.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="mes_parcelles.csv"'
        return response
