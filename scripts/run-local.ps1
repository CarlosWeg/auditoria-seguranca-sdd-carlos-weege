$ErrorActionPreference = "Stop"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
$env:APP_SECRET_KEY = "local-development-only-" + (python -c "import secrets; print(secrets.token_hex(16))")
python -m flask --app app.main run --host 127.0.0.1 --port 8000
