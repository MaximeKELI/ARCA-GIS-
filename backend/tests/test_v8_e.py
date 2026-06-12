import pytest
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient

from incidents.models import Incident
from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def farmer(db):
    return User.objects.create_user(username="e8f", password="x", role=User.Role.FARMER)


@pytest.mark.django_db
def test_health_endpoint(client):
    resp = client.get("/api/core/health/")
    assert resp.status_code == 200
    assert resp.data["status"] == "ok"
    assert resp.data["version"] == "7.7.0"
    assert resp.data["db"] is True


@pytest.mark.django_db
def test_metrics_endpoint(client, farmer):
    client.get("/api/core/health/")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "http_requests_total" in resp.content.decode()
    assert "arca_db_up" in resp.content.decode()


@pytest.mark.django_db
def test_metrics_sos_gauge(client, farmer):
    Incident.objects.create(
        reporter=farmer,
        incident_type="sos",
        title="SOS Test",
        description="Urgence",
        location=Point(-5.03, 7.69, srid=4326),
        is_sos=True,
        status="pending",
    )
    resp = client.get("/metrics")
    body = resp.content.decode()
    assert "arca_active_sos 1" in body


@pytest.mark.django_db
def test_health_unauthenticated(client):
    resp = client.get("/api/core/health/")
    assert resp.status_code == 200
