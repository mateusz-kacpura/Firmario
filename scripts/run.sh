#!/bin/bash

# Uruchom migracje Alembic
echo "Running database migrations..."
alembic upgrade head

# Uruchom aplikację FastAPI za pomocą Uvicorn
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload