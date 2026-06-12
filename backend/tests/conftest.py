import pytest
from django.contrib.gis.geos import Polygon
from rest_framework.test import APIClient

from parcels.models import Parcel
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def farmer(db):
    return User.objects.create_user(
        username="farmer_test",
        password="testpass123",
        email="farmer@test.ci",
        role=User.Role.FARMER,
    )


@pytest.fixture
def other_farmer(db):
    return User.objects.create_user(
        username="other_farmer",
        password="testpass123",
        email="other@test.ci",
        role=User.Role.FARMER,
    )


@pytest.fixture
def rescue_user(db):
    return User.objects.create_user(
        username="rescue_test",
        password="testpass123",
        role=User.Role.RESCUE,
    )


@pytest.fixture
def parcel_polygon():
    return Polygon(
        ((-5.03, 7.69), (-5.02, 7.69), (-5.02, 7.70), (-5.03, 7.70), (-5.03, 7.69)),
        srid=4326,
    )


@pytest.fixture
def farmer_parcel(farmer, parcel_polygon):
    return Parcel.objects.create(
        owner=farmer,
        name="Champ Nord",
        crop_type=Parcel.CropType.MAIZE,
        geometry=parcel_polygon,
        soil_moisture=55.0,
    )


