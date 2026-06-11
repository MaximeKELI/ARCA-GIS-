import json

from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AuditLog


class ConsentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        consents = request.data.get("consents", {})
        AuditLog.objects.create(
            user=user, action="gdpr_consent", resource="user",
            resource_id=str(user.id), details=consents,
        )
        return Response({"status": "consent recorded", "consents": consents})


class DataExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        from parcels.models import Parcel
        from incidents.models import Incident

        data = {
            "user": {
                "username": user.username, "email": user.email,
                "role": user.role, "country": user.country,
            },
            "parcels": list(Parcel.objects.filter(owner=user).values("name", "crop_type", "area_hectares")),
            "incidents": list(Incident.objects.filter(reporter=user).values("title", "status", "created_at")),
        }
        response = HttpResponse(json.dumps(data, indent=2, default=str), content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="arca_gis_data_{user.username}.json"'
        return response


class DataDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.data.get("confirm") != "DELETE_MY_DATA":
            return Response({"error": 'Envoyez {"confirm": "DELETE_MY_DATA"}'}, status=400)
        user = request.user
        AuditLog.objects.create(user=user, action="gdpr_delete_request", resource="user", resource_id=str(user.id))
        user.is_active = False
        user.save()
        return Response({"status": "Compte désactivé. Suppression complète sous 30 jours."})
