import pytest
from django.contrib.gis.geos import Polygon

from parcels.models import Parcel

from .conftest import parcel_geojson_payload


@pytest.mark.django_db
def test_list_parcels_requires_auth(api_client):
    resp = api_client.get("/api/parcels/")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_farmer_lists_only_own_parcels(api_client, farmer, other_farmer, parcel_polygon):
    Parcel.objects.create(
        owner=farmer,
        name="Ma parcelle",
        crop_type="maize",
        geometry=parcel_polygon,
    )
    Parcel.objects.create(
        owner=other_farmer,
        name="Parcelle voisine",
        crop_type="rice",
        geometry=parcel_polygon,
    )
    api_client.force_authenticate(user=farmer)
    resp = api_client.get("/api/parcels/")

    assert resp.status_code == 200
    names = [p["name"] for p in resp.data["results"]]
    assert names == ["Ma parcelle"]


@pytest.mark.django_db
def test_farmer_creates_parcel(api_client, farmer):
    api_client.force_authenticate(user=farmer)
    resp = api_client.post(
        "/api/parcels/",
        parcel_geojson_payload(name="Champ Sud"),
        format="json",
    )

    assert resp.status_code == 201
    parcel = Parcel.objects.get(name="Champ Sud")
    assert parcel.owner == farmer
    assert parcel.crop_type == "maize"
    assert parcel.area_hectares > 0


@pytest.mark.django_db
def test_rescue_cannot_create_parcel(api_client, rescue_user):
    api_client.force_authenticate(user=rescue_user)
    resp = api_client.post(
        "/api/parcels/",
        parcel_geojson_payload(),
        format="json",
    )
    assert resp.status_code == 403


@pytest.mark.django_db
def test_get_parcel_detail(api_client, farmer, farmer_parcel):
    api_client.force_authenticate(user=farmer)
    resp = api_client.get(f"/api/parcels/{farmer_parcel.id}/")

    assert resp.status_code == 200
    assert resp.data["properties"]["name"] == "Champ Nord"


@pytest.mark.django_db
def test_farmer_cannot_access_other_parcel(api_client, farmer, other_farmer, parcel_polygon):
    other = Parcel.objects.create(
        owner=other_farmer,
        name="Privée",
        crop_type="maize",
        geometry=parcel_polygon,
    )
    api_client.force_authenticate(user=farmer)
    resp = api_client.get(f"/api/parcels/{other.id}/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_farmer_updates_own_parcel(api_client, farmer, farmer_parcel):
    api_client.force_authenticate(user=farmer)
    resp = api_client.patch(
        f"/api/parcels/{farmer_parcel.id}/",
        {"properties": {"name": "Champ Renommé", "soil_moisture": 42.0}},
        format="json",
    )

    assert resp.status_code == 200
    farmer_parcel.refresh_from_db()
    assert farmer_parcel.name == "Champ Renommé"
    assert farmer_parcel.soil_moisture == 42.0


@pytest.mark.django_db
def test_farmer_deletes_own_parcel(api_client, farmer, farmer_parcel):
    api_client.force_authenticate(user=farmer)
    parcel_id = farmer_parcel.id
    resp = api_client.delete(f"/api/parcels/{parcel_id}/")

    assert resp.status_code == 204
    assert not Parcel.objects.filter(id=parcel_id).exists()


@pytest.mark.django_db
def test_nearby_parcels(api_client, farmer, farmer_parcel):
    api_client.force_authenticate(user=farmer)
    resp = api_client.get("/api/parcels/nearby/?lat=7.695&lng=-5.025&radius=10")

    assert resp.status_code == 200
    assert len(resp.data["results"]) >= 1
