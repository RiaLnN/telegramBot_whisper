release: alembic upgrade head
worker: python main.py
celery_worker: celery -A bot.tasks worker --loglevel=info