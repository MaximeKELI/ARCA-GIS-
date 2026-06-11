from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.views import DashboardStatsView
from climate.views import ClimateEventListCreateView
from partners.authentication import PartnerAPIKeyAuthentication
from users.permissions import IsAdmin

from .models import PartnerAPIKey
from .serializers import PartnerKeySerializer


class PartnerKeyListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        keys = PartnerAPIKey.objects.all()
        return Response(PartnerKeySerializer(keys, many=True).data)

    def post(self, request):
        serializer = PartnerKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.save()
        return Response(PartnerKeySerializer(key).data, status=201)


class PartnerDataView(APIView):
    authentication_classes = [PartnerAPIKeyAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        partner = request.auth
        from climate.models import ClimateEvent
        from parcels.models import Parcel
        return Response({
            "partner": partner.name,
            "data": {
                "active_climate_events": ClimateEvent.objects.filter(is_active=True).count(),
                "total_parcels": Parcel.objects.filter(is_active=True).count(),
            },
        })
