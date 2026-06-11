import pytest
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def farmer_user(db):
    user = User.objects.create_user(
        username="testfarmer", password="testpass123",
        role=User.Role.FARMER, country="Côte d'Ivoire",
    )
    user.last_position = Point(-5.03, 7.69, srid=4326)
    user.save()
    return user


@pytest.mark.django_db
def test_health_and_auth(api_client, farmer_user):
    api_client.force_authenticate(user=farmer_user)
    resp = api_client.get("/api/analytics/dashboard/")
    assert resp.status_code == 200
    assert "parcels" in resp.data


@pytest.mark.django_db
def test_subscriptions_plans(api_client, farmer_user):
    from subscriptions.models import Plan
    Plan.objects.create(name="Gratuit", tier="free", price_monthly=0)
    api_client.force_authenticate(user=farmer_user)
    resp = api_client.get("/api/subscriptions/plans/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_gdpr_export(api_client, farmer_user):
    api_client.force_authenticate(user=farmer_user)
    resp = api_client.get("/api/core/gdpr/export/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_climate_calendar(api_client, farmer_user):
    from climate.models import CropCalendar
    CropCalendar.objects.create(
        crop_type="maize", crop_name="Maïs", region="Bouaké",
        planting_start="04-01", planting_end="05-15",
        harvest_start="08-01", harvest_end="09-30",
    )
    api_client.force_authenticate(user=farmer_user)
    resp = api_client.get("/api/climate/calendar/")
    assert resp.status_code == 200
    assert len(resp.data) >= 1
