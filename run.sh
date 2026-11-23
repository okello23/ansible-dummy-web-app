#!/usr/bin/env bash
set -e

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment if present
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Default port
PORT=${PORT:-5000}

echo "=========================================================="
echo " Starting Application Server"
echo " Configuration loaded from .env"
echo " Dashboard available at: http://localhost:${PORT}"
echo " Default Login: check .env (ADMIN_USERNAME / ADMIN_PASSWORD)"
echo "=========================================================="

python3 app.py
