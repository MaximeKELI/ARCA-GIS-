from django.db.models import Sum
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from parcels.models import Parcel

from .models import BudgetEntry, CropSeason, FarmTask, FieldJournal, HarvestJournal, InputInventory
from .serializers import (
    BudgetEntrySerializer, CropSeasonSerializer, FarmTaskSerializer,
    FieldJournalSerializer, HarvestJournalSerializer, InputInventorySerializer,
)
from .task_generator import generate_tasks_from_calendar


class CropSeasonListCreateView(generics.ListCreateAPIView):
    serializer_class = CropSeasonSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["parcel", "year", "crop_type"]

    def get_queryset(self):
        u = self.request.user
        qs = CropSeason.objects.select_related("parcel")
        return qs if u.is_admin_user else qs.filter(parcel__owner=u)


class HarvestJournalListCreateView(generics.ListCreateAPIView):
    serializer_class = HarvestJournalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        qs = HarvestJournal.objects.select_related("parcel")
        return qs if u.is_admin_user else qs.filter(owner=u)


class HarvestStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = HarvestJournal.objects.filter(owner=request.user)
        by_year = {}
        for h in qs:
            y = str(h.harvest_date.year)
            by_year[y] = by_year.get(y, 0) + h.quantity_kg
        by_crop = dict(qs.values("crop_type").annotate(t=Sum("quantity_kg")).values_list("crop_type", "t"))
        return Response({"by_year": by_year, "by_crop": by_crop, "total_kg": qs.aggregate(t=Sum("quantity_kg"))["t"] or 0})


class FieldJournalListCreateView(generics.ListCreateAPIView):
    serializer_class = FieldJournalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FieldJournal.objects.filter(author=self.request.user)


class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = InputInventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InputInventory.objects.filter(owner=self.request.user)


class InventoryAlertsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        low = [i for i in InputInventory.objects.filter(owner=request.user) if i.is_low]
        return Response({"low_stock": InputInventorySerializer(low, many=True).data})


class FarmTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = FarmTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FarmTask.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FarmTaskCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            task = FarmTask.objects.get(pk=pk, owner=request.user)
        except FarmTask.DoesNotExist:
            return Response({"error": "Tâche introuvable"}, status=404)
        task.status = FarmTask.Status.DONE
        task.save()
        return Response(FarmTaskSerializer(task).data)


class GenerateTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        created = generate_tasks_from_calendar(request.user)
        return Response({"created": created})


class BudgetListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BudgetEntry.objects.filter(owner=self.request.user)


class BudgetSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = BudgetEntry.objects.filter(owner=request.user)
        income = qs.filter(entry_type="income").aggregate(t=Sum("amount"))["t"] or 0
        expense = qs.filter(entry_type="expense").aggregate(t=Sum("amount"))["t"] or 0
        return Response({"income": float(income), "expense": float(expense), "balance": float(income - expense)})


class LoanCalculatorView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        principal = float(request.data.get("principal", 100000))
        rate = float(request.data.get("annual_rate", 5)) / 100 / 12
        months = int(request.data.get("months", 12))
        if rate == 0:
            payment = principal / months
        else:
            payment = principal * (rate * (1 + rate) ** months) / ((1 + rate) ** months - 1)
        return Response({
            "monthly_payment": round(payment, 2),
            "total_paid": round(payment * months, 2),
            "total_interest": round(payment * months - principal, 2),
        })


class ParcelCompareView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        ids = request.query_params.get("ids", "").split(",")
        parcels = Parcel.objects.filter(id__in=ids, owner=request.user)
        return Response([{
            "id": p.id, "name": p.name, "crop": p.crop_type,
            "health": p.health_status, "moisture": p.soil_moisture,
            "area_ha": p.area_hectares,
        } for p in parcels])
