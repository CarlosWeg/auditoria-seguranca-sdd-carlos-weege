import os
import secrets

from flask import Flask, abort, render_template, request, session

from app.risk import RiskInput, evaluate_risk

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("APP_SECRET_KEY") or secrets.token_hex(32),
    MAX_CONTENT_LENGTH=16 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

ALLOWED_EXPOSURE = {"internal", "internet"}
ALLOWED_CRITICALITY = {"low", "medium", "high"}


def _csrf_token() -> str:
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


@app.context_processor
def inject_csrf_token() -> dict[str, object]:
    return {"csrf_token": _csrf_token}


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self'; img-src 'self' data:; "
        "base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
    )
    return response


@app.get("/")
def index():
    return render_template("index.html", result=None, errors=())


@app.post("/analyze")
def analyze():
    form_token = request.form.get("csrf_token", "")
    session_token = session.get("csrf_token", "")
    if not form_token or not session_token or not secrets.compare_digest(form_token, session_token):
        abort(400, description="Token CSRF inválido.")

    asset_name = request.form.get("asset_name", "").strip()
    exposure = request.form.get("exposure", "")
    criticality = request.form.get("criticality", "")
    sensitive_data = request.form.get("sensitive_data") == "yes"
    mfa_enabled = request.form.get("mfa_enabled") == "yes"

    errors: list[str] = []
    if not (2 <= len(asset_name) <= 80):
        errors.append("O nome do ativo deve ter entre 2 e 80 caracteres.")
    if exposure not in ALLOWED_EXPOSURE:
        errors.append("Exposição inválida.")
    if criticality not in ALLOWED_CRITICALITY:
        errors.append("Criticidade inválida.")

    if errors:
        return render_template("index.html", result=None, errors=tuple(errors)), 400

    result = evaluate_risk(
        RiskInput(
            asset_name=asset_name,
            exposure=exposure,  # type: ignore[arg-type]
            sensitive_data=sensitive_data,
            mfa_enabled=mfa_enabled,
            criticality=criticality,  # type: ignore[arg-type]
        )
    )
    return render_template("index.html", result=result, errors=(), asset_name=asset_name)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "minirisk"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
