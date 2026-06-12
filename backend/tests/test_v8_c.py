import pytest
from datetime import date, timedelta
from django.contrib.gis.geos import Polygon
from django.utils import timezone
from rest_framework.test import APIClient

from alerts.models import Alert
from farm_ops.models import BudgetEntry, HarvestJournal
from parcels.models import Parcel
from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def farmer(db):
    return User.objects.create_user(username="c8f", password="x", role=User.Role.FARMER)


@pytest.fixture
def parcel(farmer):
    poly = Polygon(
        ((-5.03, 7.69), (-5.02, 7.69), (-5.02, 7.70), (-5.03, 7.70), (-5.03, 7.69)),
        srid=4326,
    )
    return Parcel.objects.create(
        owner=farmer,
        name="Parcelle Test",
        crop_type="maize",
        geometry=poly,
        area_hectares=1.5,
        soil_moisture=65,
        health_status="good",
    )


@pytest.mark.django_db
def test_advanced_stats_endpoint(client, farmer, parcel):
    HarvestJournal.objects.create(
        parcel=parcel,
        owner=farmer,
        crop_type="maize",
        quantity_kg=120,
        harvest_date=date.today(),
    )
    BudgetEntry.objects.create(
        owner=farmer,
        entry_type="income",
        category="vente",
        amount=50000,
        entry_date=date.today(),
    )
    BudgetEntry.objects.create(
        owner=farmer,
        entry_type="expense",
        category="intrants",
        amount=15000,
        entry_date=date.today(),
    )
    Alert.objects.create(
        alert_type="climate",
        severity="medium",
        title="Test alerte",
        message="Pluie forte",
        is_broadcast=True,
    )

    client.force_authenticate(user=farmer)
    resp = client.get("/api/analytics/advanced/?months=12&metric=moisture")
    assert resp.status_code == 200
    data = resp.data
    assert "choropleth" in data
    assert "sankey" in data
    assert "timeline" in data
    assert "season_compare" in data
    assert "alerts_weekly" in data
    assert len(data["choropleth"]) >= 1
    assert data["sankey"]["total_income"] == 50000
    assert len(data["alerts_weekly"]) == 8


@pytest.mark.django_db
def test_advanced_stats_health_metric(client, farmer, parcel):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/analytics/advanced/?metric=health")
    assert resp.status_code == 200
    cell = resp.data["choropleth"][0]
    assert cell["metric"] == "health"
    assert cell["value"] > 0


@pytest.mark.django_db
def test_advanced_stats_filters(client, farmer, parcel):
    client.force_authenticate(user=farmer)
    resp = client.get(f"/api/analytics/advanced/?parcel={parcel.id}&crop=maize&months=6")
    assert resp.status_code == 200
    assert resp.data["filters"]["parcel"] == str(parcel.id)
    assert resp.data["filters"]["crop"] == "maize"
    assert resp.data["filters"]["months"] == 6


@pytest.mark.django_db
def test_advanced_stats_unauthenticated(client):
    resp = client.get("/api/analytics/advanced/")
    assert resp.status_code == 401
