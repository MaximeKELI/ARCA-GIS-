import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def farmer(db):
    return User.objects.create_user(username="b8f", password="x", role=User.Role.FARMER)


@pytest.mark.django_db
def test_agro_beekeeping(client, farmer):
    from django.contrib.gis.geos import Point
    from agro_extensions.models import BeeHive
    BeeHive.objects.create(name="Ruche Test", owner=farmer, location=Point(-5.03, 7.69, srid=4326))
    client.force_authenticate(user=farmer)
    resp = client.get("/api/agro/beekeeping/hives/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_agro_seedbank(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/agro/seedbank/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_resilience_refuges(client):
    from django.contrib.gis.geos import Point
    from resilience.models import RefugeCenter
    RefugeCenter.objects.create(name="Refuge Test", center_type="school",
                                location=Point(-5.03, 7.69, srid=4326), region="Bouaké")
    resp = client.get("/api/resilience/refuges/")
    assert resp.status_code == 200
    assert len(resp.data) >= 1


@pytest.mark.django_db
def test_resilience_drought_ews(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/resilience/drought-ews/?region=Bouaké")
    assert resp.status_code == 200
    assert "risk_level" in resp.data


@pytest.mark.django_db
def test_carbon_credits(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.get("/api/carbon/credits/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_carbon_estimate(client, farmer):
    client.force_authenticate(user=farmer)
    resp = client.post("/api/carbon/estimate/", {"area_hectares": 2, "crop_type": "maize"}, format="json")
    assert resp.status_code == 200
    assert "co2_tons_year" in resp.data
