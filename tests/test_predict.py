import requests


def test_predict_success(base_url, auth_header):
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
        headers=auth_header,
        timeout=10,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "chance_of_admit" in data
    assert isinstance(data["chance_of_admit"], (int, float))


def test_predict_missing_token(base_url):
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
        timeout=10,
    )
    assert resp.status_code == 401


def test_predict_invalid_token(base_url):
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
        headers={"Authorization": "Bearer invalid-token"},
        timeout=10,
    )
    assert resp.status_code == 401