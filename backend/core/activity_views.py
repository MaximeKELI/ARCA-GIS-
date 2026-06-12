from django.utils import timezone

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from farm_ops.models import FarmTask, FieldJournal, HarvestJournal
from parcels.history_models import ParcelChangeLog


class ActivityFeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        items = []

        for h in HarvestJournal.objects.filter(owner=user).order_by("-created_at")[:10]:
            items.append({
                "type": "harvest", "title": f"Récolte {h.quantity_kg} kg {h.crop_type}",
                "date": h.harvest_date.isoformat(), "at": h.created_at.isoformat(),
            })
        for j in FieldJournal.objects.filter(author=user).order_by("-created_at")[:10]:
            items.append({
                "type": "journal", "title": j.observation[:80],
                "date": j.entry_date.isoformat(), "at": j.created_at.isoformat(),
            })
        for t in FarmTask.objects.filter(owner=user, status="done").order_by("-created_at")[:10]:
            items.append({
                "type": "task", "title": t.title,
                "date": t.due_date.isoformat(), "at": t.created_at.isoformat(),
            })
        for log in ParcelChangeLog.objects.filter(
            parcel__owner=user, changed_at__gte=timezone.now() - timezone.timedelta(days=30),
        ).order_by("-changed_at")[:10]:
            items.append({
                "type": "parcel_change", "title": f"{log.parcel.name}: {log.field_name}",
                "date": log.changed_at.date().isoformat(), "at": log.changed_at.isoformat(),
            })

        items.sort(key=lambda x: x["at"], reverse=True)
        return Response(items[:30])
