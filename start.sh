#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
python /app/wait_for_db.py

echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT:-8000}
