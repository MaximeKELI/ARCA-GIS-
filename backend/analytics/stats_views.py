from calendar import month_abbr
from collections import defaultdict
from datetime import timedelta

from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import Alert
from climate.models import ClimateEvent, WeatherReading
from farm_ops.models import BudgetEntry, FarmTask, HarvestJournal, InputInventory
from incidents.models import Incident
from marketplace.models import MarketPrice
from parcels.models import Parcel

from .models import CropHistory


class VisualStatsView(APIView):
    """Statistiques complètes pour visualisations modernes (courbes, barres, radar, KPIs)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        is_admin = user.is_admin_user
        now = timezone.now()
        year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        parcels = Parcel.objects.filter(is_active=True)
        if not is_admin:
            parcels = parcels.filter(owner=user)

        harvests = HarvestJournal.objects.all()
        budgets = BudgetEntry.objects.all()
        tasks = FarmTask.objects.all()
        inventory = InputInventory.objects.all()
        history = CropHistory.objects.filter(recorded_at__gte=now - timedelta(days=90))
        if not is_admin:
            harvests = harvests.filter(owner=user)
            budgets = budgets.filter(owner=user)
            tasks = tasks.filter(owner=user)
            inventory = inventory.filter(owner=user)
            history = history.filter(parcel__owner=user)

        # ── KPIs ──
        total_harvest = harvests.aggregate(t=Sum("quantity_kg"))["t"] or 0
        prev_harvest = harvests.filter(
            harvest_date__gte=year_start - timedelta(days=365),
            harvest_date__lt=year_start,
        ).aggregate(t=Sum("quantity_kg"))["t"] or 0
        harvest_delta = _pct_change(total_harvest, prev_harvest)

        avg_moisture = parcels.aggregate(a=Avg("soil_moisture"))["a"] or 0
        income = budgets.filter(entry_type="income").aggregate(t=Sum("amount"))["t"] or 0
        expense = budgets.filter(entry_type="expense").aggregate(t=Sum("amount"))["t"] or 0
        pending_tasks = tasks.filter(status="pending").count()
        low_stock = sum(1 for i in inventory if i.is_low)

        kpis = [
            {"key": "parcels", "label": "Parcelles", "value": parcels.count(),
             "delta": None, "unit": "", "color": "#2E7D32", "icon": "agriculture"},
            {"key": "harvest", "label": "Récoltes", "value": round(total_harvest, 1),
             "delta": harvest_delta, "unit": "kg", "color": "#FF6F00", "icon": "grass"},
            {"key": "moisture", "label": "Humidité moy.", "value": round(avg_moisture, 1),
             "delta": None, "unit": "%", "color": "#1565C0", "icon": "water_drop"},
            {"key": "balance", "label": "Solde budget", "value": round(float(income - expense), 0),
             "delta": None, "unit": "XOF", "color": "#6A1B9A", "icon": "account_balance"},
            {"key": "tasks", "label": "Tâches", "value": pending_tasks,
             "delta": None, "unit": "en attente", "color": "#00838F", "icon": "task_alt"},
            {"key": "alerts", "label": "Alertes", "value": Alert.objects.filter(is_read=False).count(),
             "delta": None, "unit": "non lues", "color": "#D32F2F", "icon": "notifications"},
        ]

        # ── Séries temporelles ──
        moisture_trend = _monthly_series(history, "soil_moisture", now)
        if not moisture_trend:
            moisture_trend = _fallback_moisture(parcels, now)

        ndvi_trend = _monthly_series(history, "ndvi_score", now, default=0.65)
        harvest_monthly = _harvest_monthly(harvests, now)
        budget_series = _budget_monthly(budgets, now)
        rainfall = _rainfall_series(now)

        # ── Distributions ──
        crop_dist = [{"name": _crop_label(k), "value": v} for k, v in
                     parcels.values("crop_type").annotate(c=Count("id")).values_list("crop_type", "c")]
        health_dist = [{"name": _health_label(k), "value": v} for k, v in
                       parcels.values("health_status").annotate(c=Count("id")).values_list("health_status", "c")]
        task_dist = [{"name": _task_label(k), "value": v} for k, v in
                     tasks.values("status").annotate(c=Count("id")).values_list("status", "c")]
        budget_cats = [{"name": b["category"], "value": float(b["total"])} for b in
                       budgets.filter(entry_type="expense").values("category").annotate(total=Sum("amount")).order_by("-total")[:6]]

        # ── Radar farm health ──
        health_score = _health_score(health_dist)
        stock_score = max(0, 1 - low_stock / max(inventory.count(), 1))
        task_score = 1 - pending_tasks / max(tasks.count(), 1) if tasks.count() else 1
        radar = {
            "labels": ["Humidité", "Santé", "Récoltes", "Stock", "Tâches"],
            "values": [
                round(min(avg_moisture / 100, 1), 2),
                round(health_score, 2),
                round(min(total_harvest / 1000, 1), 2),
                round(stock_score, 2),
                round(task_score, 2),
            ],
        }

        # ── Sparklines (7 derniers points) ──
        spark_moisture = [h.soil_moisture for h in history.order_by("recorded_at")[:7]]
        if len(spark_moisture) < 7:
            spark_moisture = (spark_moisture + [avg_moisture] * 7)[:7]

        # ── Prix marché ──
        market = [{"crop": p.crop_type, "price": float(p.price_per_kg), "region": p.region}
                  for p in MarketPrice.objects.all()[:8]]

        # ── Incidents / climat ──
        incidents_qs = Incident.objects.all() if is_admin else Incident.objects.filter(reporter=user)
        climate_events = ClimateEvent.objects.filter(is_active=True).count()

        return Response({
            "generated_at": now.isoformat(),
            "kpis": kpis,
            "series": {
                "moisture_trend": moisture_trend,
                "ndvi_trend": ndvi_trend,
                "harvest_monthly": harvest_monthly,
                "budget_income": budget_series["income"],
                "budget_expense": budget_series["expense"],
                "rainfall": rainfall,
            },
            "distributions": {
                "crop_types": crop_dist,
                "health_status": health_dist,
                "task_status": task_dist or [{"name": "À faire", "value": 0}],
                "budget_categories": budget_cats or [{"name": "—", "value": 0}],
            },
            "radar": radar,
            "sparklines": {"moisture": spark_moisture},
            "market_prices": market,
            "summary": {
                "total_area_ha": round(parcels.aggregate(t=Sum("area_hectares"))["t"] or 0, 2),
                "active_sos": incidents_qs.filter(is_sos=True, status__in=["pending", "acknowledged", "in_progress"]).count(),
                "climate_events": climate_events,
                "low_stock_items": low_stock,
            },
        })


def _pct_change(current, previous):
    if not previous:
        return None
    return round((current - previous) / previous * 100, 1)


def _monthly_series(qs, field, now, default=0):
    months = []
    for i in range(5, -1, -1):
        start = (now.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        end = (start + timedelta(days=32)).replace(day=1)
        avg = qs.filter(recorded_at__gte=start, recorded_at__lt=end).aggregate(a=Avg(field))["a"]
        label = month_abbr[start.month]
        months.append({"label": label, "value": round(avg or default, 2)})
    return months


def _fallback_moisture(parcels, now):
    avg = parcels.aggregate(a=Avg("soil_moisture"))["a"] or 50
    return [{"label": month_abbr[(now.month - i - 1) % 12 + 1], "value": round(avg + (i - 2) * 2, 1)}
            for i in range(5, -1, -1)]


def _harvest_monthly(harvests, now):
    data = defaultdict(float)
    for h in harvests.filter(harvest_date__gte=now.date() - timedelta(days=365)):
        data[h.harvest_date.month] += h.quantity_kg
    return [{"label": month_abbr[m], "value": round(data.get(m, 0), 1)} for m in range(1, 13)]


def _budget_monthly(budgets, now):
    income, expense = [], []
    for i in range(5, -1, -1):
        start = (now.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        end = (start + timedelta(days=32)).replace(day=1)
        inc = budgets.filter(entry_type="income", entry_date__gte=start.date(), entry_date__lt=end.date()).aggregate(t=Sum("amount"))["t"] or 0
        exp = budgets.filter(entry_type="expense", entry_date__gte=start.date(), entry_date__lt=end.date()).aggregate(t=Sum("amount"))["t"] or 0
        income.append({"label": month_abbr[start.month], "value": round(float(inc), 0)})
        expense.append({"label": month_abbr[start.month], "value": round(float(exp), 0)})
    return {"income": income, "expense": expense}


def _rainfall_series(now):
    readings = WeatherReading.objects.filter(
        recorded_at__gte=now - timedelta(days=180),
    ).order_by("recorded_at")
    monthly = defaultdict(float)
    for r in readings:
        if r.rainfall_mm:
            monthly[r.recorded_at.month] += r.rainfall_mm
    if not monthly:
        return [{"label": month_abbr[m], "value": [0, 15, 45, 80, 120, 90, 60, 40, 70, 100, 50, 20][m - 1]}
                for m in range(1, 13)]
    return [{"label": month_abbr[m], "value": round(monthly.get(m, 0), 1)} for m in range(1, 13)]


def _health_score(health_dist):
    weights = {"good": 1.0, "moderate": 0.6, "poor": 0.3, "critical": 0.1}
    total = sum(d["value"] for d in health_dist) or 1
    return sum(weights.get(d["name"].lower(), 0.5) * d["value"] for d in health_dist) / total


def _crop_label(v):
    return {"maize": "Maïs", "rice": "Riz", "cassava": "Manioc", "cocoa": "Cacao"}.get(v, v)


def _health_label(v):
    return {"good": "Bon", "moderate": "Modéré", "poor": "Faible", "critical": "Critique"}.get(v, v)


def _task_label(v):
    return {"pending": "À faire", "done": "Terminé", "skipped": "Ignoré"}.get(v, v)
