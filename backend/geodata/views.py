from rest_framework import generics, permissions

from .models import CommunityMapPoint, WMSLayer
from .serializers import CommunityMapPointSerializer, WMSLayerSerializer


class CommunityPointListCreateView(generics.ListCreateAPIView):
    serializer_class = CommunityMapPointSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["category", "verified"]

    def get_queryset(self):
        return CommunityMapPoint.objects.all()


class WMSLayerListView(generics.ListAPIView):
    serializer_class = WMSLayerSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = WMSLayer.objects.filter(is_active=True)
    filterset_fields = ["country"]
