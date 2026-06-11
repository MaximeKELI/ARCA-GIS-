import csv
import io

from django.db.models import Avg, Count, Sum
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import Alert
from incidents.models import Incident
from parcels.models import Parcel
from users.models import User
from users.permissions import IsAdmin


class NGOStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not (request.user.is_admin_user or request.user.role in (User.Role.NGO, User.Role.GOVERNMENT)):
            return Response({"error": "Accès réservé ONG/gouvernement"}, status=403)

        region = request.query_params.get("region")
        parcels = Parcel.objects.filter(is_active=True)
        incidents = Incident.objects.all()
        if region:
            parcels = parcels.filter(owner__region=region)
            incidents = incidents.filter(reporter__region=region)

        return Response({
            "region": region or "national",
            "farmers": User.objects.filter(role=User.Role.FARMER).count(),
            "parcels": {
                "total": parcels.count(),
                "total_area_ha": parcels.aggregate(s=Sum("area_hectares"))["s"] or 0,
                "avg_moisture": parcels.aggregate(a=Avg("soil_moisture"))["a"],
                "by_crop": dict(parcels.values("crop_type").annotate(c=Count("id")).values_list("crop_type", "c")),
            },
            "incidents": {
                "total": incidents.count(),
                "active_sos": incidents.filter(is_sos=True, status__in=["pending", "acknowledged", "in_progress"]).count(),
                "by_status": dict(incidents.values("status").annotate(c=Count("id")).values_list("status", "c")),
            },
            "alerts": Alert.objects.count(),
        })


class NGOExportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        fmt = request.query_params.get("format", "csv")
        parcels = Parcel.objects.filter(is_active=True).select_related("owner")

        if fmt == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Parcelle", "Propriétaire", "Culture", "Surface (ha)", "Santé", "Humidité", "Région"])
            for p in parcels:
                writer.writerow([
                    p.name, p.owner.get_full_name(), p.crop_type,
                    p.area_hectares, p.health_status, p.soil_moisture, p.owner.region,
                ])
            response = HttpResponse(output.getvalue(), content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="arca_gis_parcels.csv"'
            return response

        data = [{
            "name": p.name, "owner": p.owner.username, "crop": p.crop_type,
            "area_ha": p.area_hectares, "health": p.health_status,
        } for p in parcels[:500]]
        return Response({"format": "json", "count": len(data), "parcels": data})
