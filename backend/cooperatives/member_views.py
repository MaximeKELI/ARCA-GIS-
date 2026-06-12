from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cooperative


class CooperativeMembersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            coop = Cooperative.objects.get(pk=pk)
        except Cooperative.DoesNotExist:
            return Response({"error": "Coopérative introuvable"}, status=404)
        members = coop.members.all()
        return Response([{
            "id": m.id, "username": m.username,
            "name": m.get_full_name(), "role": m.role,
            "phone": m.phone, "region": m.region,
            "is_president": coop.president_id == m.id,
        } for m in members])
