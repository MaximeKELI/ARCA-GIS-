import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def farmer(db):
    return User.objects.create_user(username="v6f", password="x", role=User.Role.FARMER)


@pytest.mark.django_db
def test_pictogram_menu(client):
    resp = client.get("/api/inclusion/pictogram-menu/")
    assert resp.status_code == 200
    assert len(resp.data["items"]) >= 4


@pytest.mark.django_db
def test_refuge_centers(client):
    from django.contrib.gis.geos import Point
    from resilience.models import RefugeCenter
    RefugeCenter.objects.create(name="École Test", center_type="school",
                                location=Point(-5.03, 7.69, srid=4326), region="Bouaké")
    resp = client.get("/api/resilience/refuges/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_flood_simulation(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.post("/api/resilience/flood-simulate/", {"rainfall_mm": 120, "elevation_m": 150}, format="json")
    assert resp.status_code == 200
    assert "flood_risk_pct" in resp.data


@pytest.mark.django_db
def test_oauth_providers(client):
    resp = client.get("/api/core/oauth/providers/")
    assert resp.status_code == 200
