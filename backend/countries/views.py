from rest_framework import generics, permissions

from .models import CountryConfig
from .serializers import CountryConfigSerializer


class CountryListView(generics.ListAPIView):
    serializer_class = CountryConfigSerializer
    permission_classes = [permissions.AllowAny]
    queryset = CountryConfig.objects.filter(is_active=True)
