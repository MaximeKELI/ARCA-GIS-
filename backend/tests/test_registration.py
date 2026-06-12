import pytest
from rest_framework.test import APIClient

from users.models import User
from users.serializers import UserRegistrationSerializer


@pytest.fixture
def api_client():
    return APIClient()


def _payload(**overrides):
    data = {
        "username": "nouveau_user",
        "email": "nouveau@example.ci",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Kofi",
        "last_name": "Diallo",
        "role": "farmer",
        "country": "Côte d'Ivoire",
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_registration_api_success(api_client):
    resp = api_client.post("/api/users/register/", _payload(), format="json")
    assert resp.status_code == 201
    assert resp.data["username"] == "nouveau_user"
    assert resp.data["role"] == "farmer"

    user = User.objects.get(username="nouveau_user")
    assert user.is_2fa_enabled is False
    assert user.preferred_language == "fr"
    assert user.totp_secret == ""
    assert user.check_password("testpass123")


@pytest.mark.django_db
def test_registration_api_password_mismatch(api_client):
    resp = api_client.post(
        "/api/users/register/",
        _payload(password_confirm="autre_mot_de_passe"),
        format="json",
    )
    assert resp.status_code == 400
    assert "password" in resp.data


@pytest.mark.django_db
def test_registration_api_restricted_role(api_client):
    resp = api_client.post(
        "/api/users/register/",
        _payload(username="hacker", role="admin"),
        format="json",
    )
    assert resp.status_code == 400
    assert "role" in resp.data


@pytest.mark.django_db
def test_registration_api_duplicate_username(api_client):
    User.objects.create_user(username="doublon", password="testpass123", role=User.Role.FARMER)
    resp = api_client.post(
        "/api/users/register/",
        _payload(username="doublon", email="autre@example.ci"),
        format="json",
    )
    assert resp.status_code == 400
    assert "username" in resp.data


@pytest.mark.django_db
def test_registration_serializer_sets_defaults():
    serializer = UserRegistrationSerializer(data=_payload(username="serial_user", email="s@t.com"))
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()

    assert user.is_2fa_enabled is False
    assert user.preferred_language == "fr"
    assert user.totp_secret == ""
    assert user.role == User.Role.FARMER


@pytest.mark.django_db
def test_user_manager_create_user_defaults():
    user = User.objects.create_user(
        username="mgr_user",
        email="mgr@t.com",
        password="testpass123",
        role=User.Role.RESCUE,
    )
    assert user.is_2fa_enabled is False
    assert user.preferred_language == "fr"
    assert user.totp_secret == ""
