from calendar import month_abbr
from collections import defaultdict
from datetime import timedelta

from django.db import models
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import Alert
from cooperatives.models import Cooperative
from farm_ops.models import BudgetEntry, FarmTask, FieldJournal, HarvestJournal
from parcels.history_models import ParcelChangeLog
from parcels.models import Parcel


class AdvancedStatsView(APIView):
    """Stats avancées v7.5 : choroplèthe, Sankey, timeline, saisons, alertes/semaine."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()
        months = int(request.query_params.get("months", 12))
        crop_filter = request.query_params.get("crop")
        parcel_id = request.query_params.get("parcel")
        metric = request.query_params.get("metric", "moisture")
        since = now - timedelta(days=months * 30)

        parcels = Parcel.objects.filter(is_active=True, owner=user)
        if crop_filter:
            parcels = parcels.filter(crop_type=crop_filter)
        if parcel_id:
            parcels = parcels.filter(pk=parcel_id)

        harvests = HarvestJournal.objects.filter(owner=user, harvest_date__gte=since.date())
        if crop_filter:
            harvests = harvests.filter(crop_type=crop_filter)
        if parcel_id:
            harvests = harvests.filter(parcel_id=parcel_id)

        budgets = BudgetEntry.objects.filter(owner=user, entry_date__gte=since.date())
        alerts = Alert.objects.filter(created_at__gte=since).filter(
            models.Q(target_user=user) | models.Q(target_user__isnull=True, is_broadcast=True)
        )

        return Response({
            "filters": {"months": months, "crop": crop_filter, "parcel": parcel_id, "metric": metric},
            "choropleth": _choropleth(parcels, metric),
            "sankey": _sankey(budgets),
            "timeline": _timeline(user, parcel_id, since),
            "season_compare": _season_compare(harvests),
            "alerts_weekly": _alerts_weekly(alerts, now),
            "coop_radar": _coop_radar(user),
        })


def _choropleth(parcels, metric):
    cells = []
    for p in parcels:
        if not p.geometry:
            continue
        c = p.geometry.centroid
        if metric == "health":
            val = {"good": 0.85, "moderate": 0.55, "poor": 0.35, "critical": 0.15, "excellent": 0.95}.get(p.health_status, 0.5)
            color = _interp_color(val)
        else:
            val = (p.soil_moisture or 0) / 100
            color = _interp_color(val)
        cells.append({
            "id": p.id, "name": p.name, "lat": c.y, "lng": c.x,
            "crop": p.crop_type, "value": round(val * 100, 1),
            "metric": metric, "color": color,
        })
    return cells


def _interp_color(t):
    t = max(0, min(1, t))
    r = int(255 * (1 - t))
    g = int(200 * t + 55 * (1 - t))
    return f"#{r:02x}{g:02x}33"


def _sankey(budgets):
    income = float(budgets.filter(entry_type="income").aggregate(t=Sum("amount"))["t"] or 0)
    expenses = list(budgets.filter(entry_type="expense").values("category").annotate(total=Sum("amount")).order_by("-total")[:5])
    nodes = ["Revenus"] + [e["category"] for e in expenses]
    if income == 0 and not expenses:
        return {"nodes": ["Revenus", "Dépenses"], "links": [{"source": 0, "target": 1, "value": 0}]}
    links = []
    for i, e in enumerate(expenses):
        links.append({"source": 0, "target": i + 1, "value": round(float(e["total"]), 0)})
    balance = income - sum(float(e["total"]) for e in expenses)
    if balance > 0:
        nodes.append("Épargne")
        links.append({"source": 0, "target": len(nodes) - 1, "value": round(balance, 0)})
    return {"nodes": nodes, "links": links, "total_income": round(income, 0)}


def _timeline(user, parcel_id, since):
    items = []
    harvests = HarvestJournal.objects.filter(owner=user, created_at__gte=since)
    journals = FieldJournal.objects.filter(author=user, created_at__gte=since)
    tasks = FarmTask.objects.filter(owner=user, created_at__gte=since, status="done")
    logs = ParcelChangeLog.objects.filter(changed_by=user, changed_at__gte=since)
    if parcel_id:
        harvests = harvests.filter(parcel_id=parcel_id)
        journals = journals.filter(parcel_id=parcel_id)
        tasks = tasks.filter(parcel_id=parcel_id)
        logs = logs.filter(parcel_id=parcel_id)

    for h in harvests[:15]:
        items.append({"type": "harvest", "date": h.harvest_date.isoformat(), "at": h.created_at.isoformat(),
                      "title": f"Récolte {h.quantity_kg} kg {h.crop_type}", "icon": "agriculture"})
    for j in journals[:15]:
        items.append({"type": "journal", "date": j.entry_date.isoformat(), "at": j.created_at.isoformat(),
                      "title": j.observation[:80], "icon": "menu_book"})
    for t in tasks[:10]:
        items.append({"type": "task", "date": t.due_date.isoformat(), "at": t.created_at.isoformat(),
                      "title": t.title, "icon": "task_alt"})
    for log in logs[:10]:
        items.append({"type": "change", "date": log.changed_at.date().isoformat(), "at": log.changed_at.isoformat(),
                      "title": f"{log.parcel.name}: {log.field_name}", "icon": "edit"})
    items.sort(key=lambda x: x["at"], reverse=True)
    return items[:40]


def _season_compare(harvests):
    by_year = defaultdict(lambda: defaultdict(float))
    for h in harvests:
        by_year[h.harvest_date.year][h.crop_type] += h.quantity_kg
    years = sorted(by_year.keys())[-3:]
    crops = sorted({c for yd in by_year.values() for c in yd})
    return {
        "years": years,
        "crops": [_crop_label(c) for c in crops],
        "data": [{ "year": y, "values": [round(by_year[y].get(c, 0), 1) for c in crops]} for y in years],
    }


def _alerts_weekly(alerts, now):
    weeks = []
    for i in range(7, -1, -1):
        start = now - timedelta(weeks=i + 1)
        end = now - timedelta(weeks=i)
        count = alerts.filter(created_at__gte=start, created_at__lt=end).count()
        weeks.append({"label": f"S{8 - i}", "value": count})
    return weeks


def _coop_radar(user):
    coop = Cooperative.objects.filter(members=user).first()
    if not coop:
        return {"labels": [], "values": [], "coop_name": None}
    member_parcels = Parcel.objects.filter(owner__in=coop.members.all(), is_active=True)
    avg_moisture = member_parcels.aggregate(a=Avg("soil_moisture"))["a"] or 0
    health_good = member_parcels.filter(health_status__in=["good", "excellent"]).count()
    health_ratio = health_good / max(member_parcels.count(), 1)
    total_harvest = HarvestJournal.objects.filter(owner__in=coop.members.all()).aggregate(t=Sum("quantity_kg"))["t"] or 0
    return {
        "coop_name": coop.name,
        "labels": ["Humidité", "Santé", "Récoltes", "Membres", "Surface"],
        "values": [
            round(min(avg_moisture / 100, 1), 2),
            round(health_ratio, 2),
            round(min(total_harvest / 2000, 1), 2),
            round(min(coop.member_count / 20, 1), 2),
            round(min((member_parcels.aggregate(t=Sum("area_hectares"))["t"] or 0) / 100, 1), 2),
        ],
    }


def _crop_label(v):
    return {"maize": "Maïs", "rice": "Riz", "cassava": "Manioc", "cocoa": "Cacao"}.get(v, v)
