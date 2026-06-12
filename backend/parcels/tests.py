from django.contrib.gis.geos import Polygon
from django.test import TestCase

from users.models import User

from .models import Parcel


class ParcelModelTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="parcel_owner",
            password="testpass123",
            role=User.Role.FARMER,
        )
        self.polygon = Polygon(
            ((-5.03, 7.69), (-5.02, 7.69), (-5.02, 7.70), (-5.03, 7.70), (-5.03, 7.69)),
            srid=4326,
        )

    def test_area_computed_on_save(self):
        parcel = Parcel.objects.create(
            owner=self.owner,
            name="Auto aire",
            crop_type="maize",
            geometry=self.polygon,
        )
        self.assertGreater(parcel.area_hectares, 0)

    def test_str_representation(self):
        parcel = Parcel.objects.create(
            owner=self.owner,
            name="Champ Test",
            crop_type="rice",
            geometry=self.polygon,
        )
        self.assertIn("Champ Test", str(parcel))
