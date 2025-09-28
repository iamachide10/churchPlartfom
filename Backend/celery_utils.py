from celery import Celery
import os
from kombu import Connection
import ssl

def make_celery(app):
    app.config.update(
    broker_url=os.getenv("broker_url", "redis://localhost:6379/0"),
    result_backend=os.getenv("result_backend", "redis://localhost:6379/0"),
    include=["tasks"],
    )

    celery = Celery(
    app.import_name,
    broker=app.config["broker_url"],
    backend=app.config["result_backend"],
    include=app.config["include"],
)

    celery.conf.update(app.config)

    # 🔑 Force SSL (important for Upstash rediss://)
    celery.conf.update(
        broker_use_ssl={
            "ssl_cert_reqs": ssl.CERT_NONE
        },
        redis_backend_use_ssl={
            "ssl_cert_reqs": ssl.CERT_NONE
        },
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
