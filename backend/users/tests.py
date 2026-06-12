from django.test import TestCase

from .models import User
from .serializers import UserRegistrationSerializer


class UserRegistrationSerializerTests(TestCase):
    def test_valid_farmer_registration(self):
        data = {
            "username": "test_farmer",
            "email": "farmer@test.ci",
            "password": "securepass1",
            "password_confirm": "securepass1",
            "first_name": "Awa",
            "last_name": "Koné",
            "role": "farmer",
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, "test_farmer")
        self.assertFalse(user.is_2fa_enabled)

    def test_password_mismatch_rejected(self):
        data = {
            "username": "bad_pw",
            "email": "bad@test.ci",
            "password": "securepass1",
            "password_confirm": "different1",
            "first_name": "X",
            "last_name": "Y",
            "role": "farmer",
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
