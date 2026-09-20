import secrets

from app.main import app


def test_home_and_security_headers():
    app.config.update(TESTING=True, SECRET_KEY=secrets.token_hex(32))
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"MiniRisk" in response.data
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]


def test_health_endpoint():
    app.config.update(TESTING=True, SECRET_KEY=secrets.token_hex(32))
    client = app.test_client()
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_analysis_requires_csrf():
    app.config.update(TESTING=True, SECRET_KEY=secrets.token_hex(32))
    client = app.test_client()
    response = client.post(
        "/analyze",
        data={
            "asset_name": "Portal",
            "exposure": "internet",
            "criticality": "high",
            "sensitive_data": "yes",
            "mfa_enabled": "no",
        },
    )
    assert response.status_code == 400


def test_valid_analysis():
    app.config.update(TESTING=True, SECRET_KEY=secrets.token_hex(32))
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["csrf_token"] = "valid-token"

    response = client.post(
        "/analyze",
        data={
            "csrf_token": "valid-token",
            "asset_name": "Portal do Cliente",
            "exposure": "internet",
            "criticality": "high",
            "sensitive_data": "yes",
            "mfa_enabled": "no",
        },
    )
    assert response.status_code == 200
    assert "Risco Alto" in response.get_data(as_text=True)
