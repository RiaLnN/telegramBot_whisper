from celery import Celery
from bot.core.config import settings

app = Celery(
    "llm_call",
    broker=settings.redis_dsn,
    backend=settings.redis_dsn,
    include=["bot.tasks"]
)


if settings.redis_dsn.startswith("rediss://"):
    import ssl
    app.conf.update(
        broker_use_ssl={'ssl_cert_reqs': ssl.CERT_NONE},
        redis_backend_use_ssl={'ssl_cert_reqs': ssl.CERT_NONE}
    )