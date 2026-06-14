import os
import requests
import pytest

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:3000")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def auth_token(base_url):
    resp = requests.post(
        f"{base_url}/login",
        json={"username": "admin", "password": "admin123"},
        timeout=10,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    return data["access_token"]


@pytest.fixture(scope="session")
def auth_header(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}