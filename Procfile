release: alembic upgrade head
worker: python bot/main.py
celery_worker: celery -A bot.core.celery worker --loglevel=info