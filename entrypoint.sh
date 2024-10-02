#!/bin/bash

# Выполняем миграции Alembic
echo "Running Alembic migrations..."
alembic upgrade head

# Запускаем приложение FastAPI
echo "Starting FastAPI application..."
exec uvicorn src.application:app --host 0.0.0.0 --port 8003 --reload
