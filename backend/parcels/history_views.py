from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .history_models import ParcelChangeLog
from .models import Parcel


class ParcelHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if not Parcel.objects.filter(pk=pk, owner=request.user).exists():
            return Response({"error": "Parcelle introuvable"}, status=404)
        logs = ParcelChangeLog.objects.filter(parcel_id=pk).order_by("-changed_at")[:50]
        return Response([{
            "field": l.field_name, "old": l.old_value, "new": l.new_value,
            "changed_at": l.changed_at.isoformat(),
            "by": l.changed_by.get_full_name() if l.changed_by else None,
        } for l in logs])
