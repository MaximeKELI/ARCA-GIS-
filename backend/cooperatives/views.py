from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cooperative
from .serializers import CooperativeSerializer


class CooperativeListCreateView(generics.ListCreateAPIView):
    queryset = Cooperative.objects.filter(is_active=True)
    serializer_class = CooperativeSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "region"]


class CooperativeDetailView(generics.RetrieveUpdateAPIView):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    permission_classes = [permissions.IsAuthenticated]


class JoinCooperativeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            coop = Cooperative.objects.get(pk=pk)
        except Cooperative.DoesNotExist:
            return Response({"error": "Coopérative introuvable"}, status=404)
        coop.members.add(request.user)
        coop.member_count = coop.members.count()
        coop.save()
        return Response(CooperativeSerializer(coop).data)
