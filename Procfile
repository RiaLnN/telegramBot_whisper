release: alembic upgrade head
worker: python bot/main.py
celery_worker: celery -A bot.tasks worker --loglevel=info