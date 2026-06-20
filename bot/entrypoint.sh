#!/bin/bash
set -e

echo "Running database migrations..."
alembic revision --autogenerate -m 'initial'
alembic upgrade head

echo "Starting Telegram bot..."
python -m bot.main