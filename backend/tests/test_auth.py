import pytest

from users.models import User


@pytest.mark.django_db
def test_login_success(api_client, farmer):
    resp = api_client.post(
        "/api/auth/token/",
        {"username": "farmer_test", "password": "testpass123"},
        format="json",
    )
    assert resp.status_code == 200
    assert "access" in resp.data
    assert "refresh" in resp.data


@pytest.mark.django_db
def test_login_wrong_password(api_client, farmer):
    resp = api_client.post(
        "/api/auth/token/",
        {"username": "farmer_test", "password": "wrong"},
        format="json",
    )
    assert resp.status_code == 401


@pytest.mark.django_db
def test_login_unknown_user(api_client):
    resp = api_client.post(
        "/api/auth/token/",
        {"username": "ghost", "password": "testpass123"},
        format="json",
    )
    assert resp.status_code == 401


@pytest.mark.django_db
def test_token_refresh(api_client, farmer):
    login = api_client.post(
        "/api/auth/token/",
        {"username": "farmer_test", "password": "testpass123"},
        format="json",
    )
    resp = api_client.post(
        "/api/auth/token/refresh/",
        {"refresh": login.data["refresh"]},
        format="json",
    )
    assert resp.status_code == 200
    assert "access" in resp.data


@pytest.mark.django_db
def test_profile_requires_authentication(api_client):
    resp = api_client.get("/api/users/profile/")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_profile_after_login(api_client, farmer):
    login = api_client.post(
        "/api/auth/token/",
        {"username": "farmer_test", "password": "testpass123"},
        format="json",
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
    resp = api_client.get("/api/users/profile/")

    assert resp.status_code == 200
    assert resp.data["username"] == "farmer_test"
    assert resp.data["role"] == User.Role.FARMER


@pytest.mark.django_db
def test_register_then_login_flow(api_client):
    register = api_client.post(
        "/api/users/register/",
        {
            "username": "flow_user",
            "email": "flow@test.ci",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "Flow",
            "last_name": "Test",
            "role": "farmer",
        },
        format="json",
    )
    assert register.status_code == 201

    login = api_client.post(
        "/api/auth/token/",
        {"username": "flow_user", "password": "testpass123"},
        format="json",
    )
    assert login.status_code == 200
