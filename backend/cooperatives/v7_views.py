from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cooperative
from .v7_models import CooperativeVote, EquipmentReservation, VoteBallot


class VoteListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        coop_id = request.query_params.get("cooperative")
        qs = CooperativeVote.objects.filter(is_open=True)
        if coop_id:
            qs = qs.filter(cooperative_id=coop_id)
        return Response([{"id": v.id, "title": v.title, "ends_at": v.ends_at.isoformat()} for v in qs])

    def post(self, request):
        v = CooperativeVote.objects.create(
            cooperative_id=request.data.get("cooperative_id"),
            title=request.data.get("title"),
            description=request.data.get("description", ""),
            created_by=request.user,
            ends_at=request.data.get("ends_at", timezone.now()),
        )
        return Response({"id": v.id}, status=201)


class CastVoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        ballot, _ = VoteBallot.objects.update_or_create(
            vote_id=pk, voter=request.user,
            defaults={"choice": request.data.get("choice")},
        )
        return Response({"status": "voted", "choice": ballot.choice})


class EquipmentReserveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = EquipmentReservation.objects.filter(cooperative__members=request.user)
        return Response([{
            "id": r.id, "equipment": r.equipment_name,
            "start": str(r.start_date), "end": str(r.end_date), "status": r.status,
        } for r in qs])

    def post(self, request):
        r = EquipmentReservation.objects.create(
            cooperative_id=request.data.get("cooperative_id"),
            equipment_name=request.data.get("equipment_name"),
            reserved_by=request.user,
            start_date=request.data.get("start_date"),
            end_date=request.data.get("end_date"),
        )
        return Response({"id": r.id}, status=201)
