import requests


def test_login_returns_bearer_token(base_url):
    resp = requests.post(
        f"{base_url}/login",
        json={"username": "admin", "password": "admin123"},
        timeout=10,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 10


def test_predict_requires_bearer_header(base_url):
    payload = {
        "GRE Score": 320,
        "TOEFL Score": 110,
        "University Rating": 4,
        "SOP": 4.5,
        "LOR": 4.0,
        "CGPA": 8.8,
        "Research": 1,
    }
    resp = requests.post(
        f"{base_url}/predict",
        json=payload,
        headers={"Authorization": "Token wrong"},
        timeout=10,
    )
    assert resp.status_code == 401