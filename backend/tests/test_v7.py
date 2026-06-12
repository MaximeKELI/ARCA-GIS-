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
def test_offline_sync(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.post("/api/core/offline/sync/", {
        "action_type": "harvest", "payload": {"crop_type": "maize", "quantity_kg": 100},
    }, format="json")
    assert resp.status_code in (200, 201)
