from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.services import broadcast_alert
from farm_ops.models import FarmTask, InputInventory
from parcels.models import Parcel

from .rule_models import AlertRule, NotificationPreference


class AlertRuleListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AlertRule.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        return Response([{
            "id": r.id, "name": r.name, "metric": r.metric,
            "operator": r.operator, "threshold": r.threshold, "is_active": r.is_active,
        } for r in self.get_queryset()])

    def create(self, request, *args, **kwargs):
        r = AlertRule.objects.create(
            owner=request.user, name=request.data.get("name"),
            metric=request.data.get("metric"), operator=request.data.get("operator", "lt"),
            threshold=request.data.get("threshold", 30),
        )
        return Response({"id": r.id}, status=201)


class NotificationPrefView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        prefs, _ = NotificationPreference.objects.get_or_create(user=request.user)
        return Response({
            "climate": prefs.climate, "crop": prefs.crop, "sos": prefs.sos, "market": prefs.market,
            "quiet_start": str(prefs.quiet_start) if prefs.quiet_start else None,
            "quiet_end": str(prefs.quiet_end) if prefs.quiet_end else None,
        })

    def patch(self, request):
        prefs, _ = NotificationPreference.objects.get_or_create(user=request.user)
        for field in ("climate", "crop", "sos", "market"):
            if field in request.data:
                setattr(prefs, field, request.data[field])
        prefs.save()
        return Response({"status": "updated"})


class EvaluateRulesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        triggered = []
        for rule in AlertRule.objects.filter(owner=request.user, is_active=True):
            if rule.metric == "soil_moisture":
                for p in Parcel.objects.filter(owner=request.user, soil_moisture__lt=rule.threshold):
                    triggered.append({"rule": rule.name, "parcel": p.name, "value": p.soil_moisture})
                    broadcast_alert("crop", f"Règle: {rule.name}", f"{p.name}: humidité {p.soil_moisture}%",
                                    "medium", {"parcel_id": p.id}, target_user=request.user)
            elif rule.metric == "inventory":
                for i in InputInventory.objects.filter(owner=request.user):
                    if i.quantity <= rule.threshold:
                        triggered.append({"rule": rule.name, "product": i.product_name})
                        broadcast_alert("crop", f"Règle: {rule.name}",
                                        f"Stock bas: {i.product_name} ({i.quantity} {i.unit})",
                                        "medium", {"product": i.product_name}, target_user=request.user)
            elif rule.metric == "task_overdue":
                for t in FarmTask.objects.filter(owner=request.user, status="pending", due_date__lt=timezone.now().date()):
                    triggered.append({"rule": rule.name, "task": t.title})
                    broadcast_alert("crop", f"Règle: {rule.name}",
                                    f"Tâche en retard: {t.title}", "medium",
                                    {"task_id": t.id}, target_user=request.user)
        return Response({"triggered": triggered, "count": len(triggered)})
