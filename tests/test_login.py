import requests


def test_login_success(base_url):
    resp = requests.post(
        f"{base_url}/login",
        json={"username": "admin", "password": "admin123"},
        timeout=10,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_credentials(base_url):
    resp = requests.post(
        f"{base_url}/login",
        json={"username": "wrong", "password": "wrong"},
        timeout=10,
    )
    assert resp.status_code in (401, 400)