#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
export APP_SECRET_KEY="local-development-only-$(python -c 'import secrets; print(secrets.token_hex(16))')"
flask --app app.main run --host 127.0.0.1 --port 8000
