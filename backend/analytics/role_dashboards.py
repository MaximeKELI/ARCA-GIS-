from django.db.models import Avg, Count, Sum
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from farm_ops.models import FarmTask, HarvestJournal
from incidents.models import Incident
from parcels.models import Parcel
from users.models import User


class FarmerDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "role": "farmer",
            "parcels": Parcel.objects.filter(owner=u, is_active=True).count(),
            "pending_tasks": FarmTask.objects.filter(owner=u, status="pending").count(),
            "harvests_kg": HarvestJournal.objects.filter(owner=u).aggregate(t=Sum("quantity_kg"))["t"] or 0,
            "avg_moisture": Parcel.objects.filter(owner=u).aggregate(a=Avg("soil_moisture"))["a"],
        })


class RescueDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "role": "rescue",
            "active_sos": Incident.objects.filter(is_sos=True, status__in=["pending", "acknowledged", "in_progress"]).count(),
            "assigned": Incident.objects.filter(assigned_to=request.user, status="in_progress").count(),
            "resolved_today": Incident.objects.filter(status="resolved").count(),
        })


class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_admin_user:
            return Response({"error": "Admin requis"}, status=403)
        return Response({
            "role": "admin",
            "users": User.objects.count(),
            "farmers": User.objects.filter(role=User.Role.FARMER).count(),
            "parcels": Parcel.objects.filter(is_active=True).count(),
            "incidents": Incident.objects.count(),
            "total_area_ha": Parcel.objects.aggregate(t=Sum("area_hectares"))["t"] or 0,
        })


class RoleDashboardRouterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        role = request.user.role
        if role == User.Role.RESCUE:
            return RescueDashboardView().get(request)
        if request.user.is_admin_user:
            return AdminDashboardView().get(request)
        return FarmerDashboardView().get(request)
