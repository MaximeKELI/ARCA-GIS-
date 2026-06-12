import base64
import pytest
from datetime import date, timedelta
from django.contrib.gis.geos import Polygon
from rest_framework.test import APIClient

from farm_ops.models import FarmTask
from parcels.models import Parcel
from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def farmer(db):
    return User.objects.create_user(username="d8f", password="x", role=User.Role.FARMER)


@pytest.fixture
def parcel(farmer):
    poly = Polygon(
        ((-5.03, 7.69), (-5.02, 7.69), (-5.02, 7.70), (-5.03, 7.70), (-5.03, 7.69)),
        srid=4326,
    )
    return Parcel.objects.create(
        owner=farmer,
        name="Parcelle IA",
        crop_type="maize",
        geometry=poly,
        area_hectares=2.0,
        soil_moisture=35,
        health_status="moderate",
    )


@pytest.mark.django_db
def test_advisor_chat(client, farmer, parcel):
    client.force_authenticate(user=farmer)
    resp = client.post("/api/ai/chat/", {"query": "irrigation maïs", "parcel_id": parcel.id}, format="json")
    assert resp.status_code == 200
    assert "response" in resp.data or "answers" in resp.data


@pytest.mark.django_db
def test_disease_detect(client, farmer):
    client.force_authenticate(user=farmer)
    img = base64.b64encode(b"fake-image-data").decode()
    resp = client.post("/api/ai/disease/", {"image_b64": img, "crop_type": "maize"}, format="json")
    assert resp.status_code == 200
    assert "diagnosis" in resp.data
    assert "treatment" in resp.data


@pytest.mark.django_db
def test_weekly_planner(client, farmer, parcel):
    FarmTask.objects.create(
        owner=farmer,
        parcel=parcel,
        title="Irriguer",
        due_date=date.today() + timedelta(days=2),
        status=FarmTask.Status.PENDING,
    )
    client.force_authenticate(user=farmer)
    resp = client.get("/api/ai/planner/")
    assert resp.status_code == 200
    assert len(resp.data["parcel_plans"]) >= 1
    assert len(resp.data["pending_tasks"]) >= 1


@pytest.mark.django_db
def test_voice_journal(client, farmer, parcel):
    client.force_authenticate(user=farmer)
    resp = client.post("/api/ai/voice-journal/", {
        "text": "Pluie modérée ce matin, feuilles en bon état.",
        "parcel_id": parcel.id,
        "save": True,
    }, format="json")
    assert resp.status_code == 200
    assert resp.data["saved"] is True
    assert resp.data["journal_id"] is not None


@pytest.mark.django_db
def test_ai_unauthenticated(client):
    resp = client.post("/api/ai/chat/", {"query": "test"}, format="json")
    assert resp.status_code == 401
