import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def farmer(db):
    return User.objects.create_user(username="v7f", password="x", role=User.Role.FARMER)


@pytest.mark.django_db
def test_farm_harvests(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/farm/harvests/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_farm_budget_summary(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/farm/budget/summary/")
    assert resp.status_code == 200
    assert "balance" in resp.data


@pytest.mark.django_db
def test_alert_rules(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/alerts/rules/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_role_dashboard(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/analytics/role-dashboard/")
    assert resp.status_code == 200
    assert "role" in resp.data


@pytest.mark.django_db
def test_ussd_simulator(client):
    resp = client.post("/api/communications/ussd/simulate/", {"text": ""}, format="json")
    assert resp.status_code == 200
    assert "response" in resp.data


@pytest.mark.django_db
def test_activity_feed(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/core/activity/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_bookmarks(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.post("/api/core/bookmarks/", {
        "resource_type": "parcel", "resource_id": 1, "label": "Test",
    }, format="json")
    assert resp.status_code in (200, 201)
    resp = client.get("/api/core/bookmarks/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_coop_members(client, farmer):
    from cooperatives.models import Cooperative
    coop = Cooperative.objects.create(name="Test Coop", country="CI", region="Bouaké")
    coop.members.add(farmer)
    client.force_authenticate(user=farmer)
    resp = client.get(f"/api/cooperatives/{coop.id}/members/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_parcel_csv_export(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/parcels/export/csv/")
    assert resp.status_code == 200
    assert "text/csv" in resp["Content-Type"]


@pytest.mark.django_db
def test_visual_stats(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/analytics/visual/")
    assert resp.status_code == 200
    assert "kpis" in resp.data
    assert "series" in resp.data
    assert "radar" in resp.data
    assert len(resp.data["kpis"]) >= 4


@pytest.mark.django_db
def test_global_search(client, farmer):
    from parcels.models import Parcel
    Parcel.objects.create(owner=farmer, name="Champ Test Search", crop_type="maize")
    client.force_authenticate(user=farmer)
    resp = client.get("/api/core/search/?q=Champ")
    assert resp.status_code == 200
    assert resp.data["count"] >= 1


@pytest.mark.django_db
def test_stats_pdf_export(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/analytics/visual/export/pdf/")
    assert resp.status_code == 200
    assert "application/pdf" in resp["Content-Type"]


@pytest.mark.django_db
def test_offline_sync(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.post("/api/core/offline/sync/", {
        "action_type": "harvest", "payload": {"crop_type": "maize", "quantity_kg": 100},
    }, format="json")
    assert resp.status_code in (200, 201)
