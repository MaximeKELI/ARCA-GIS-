import pytest
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def farmer(db):
    return User.objects.create_user(username="v5farmer", password="test1234", role=User.Role.FARMER)


@pytest.mark.django_db
def test_countries_list(api_client):
    from countries.models import CountryConfig
    CountryConfig.objects.create(code="CI", name="Côte d'Ivoire", currency="XOF")
    resp = api_client.get("/api/countries/")
    assert resp.status_code == 200
    assert len(resp.data) >= 1


@pytest.mark.django_db
def test_evacuation_checklist(api_client):
    resp = api_client.get("/api/incidents/evacuation-checklist/?type=flood")
    assert resp.status_code == 200
    assert "steps" in resp.data


@pytest.mark.django_db
def test_livestock_herd(api_client, farmer):
    api_client.force_authenticate(user=farmer)
    resp = api_client.post("/api/livestock/herds/", {
        "name": "Troupeau Test", "animal_type": "cattle", "count": 10,
    }, format="json")
    assert resp.status_code == 201


@pytest.mark.django_db
def test_finance_loan(api_client, farmer):
    api_client.force_authenticate(user=farmer)
    resp = api_client.post("/api/finance/loans/", {
        "amount": 100000, "crop_type": "maize", "purpose": "Semences",
    }, format="json")
    assert resp.status_code == 201
