from celery import Celery
import os

def make_celery(app):
    # Step 1: Load from ENV instead of hardcoding
    app.config.update(
        CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        CELERY_INCLUDE=["tasks"],  # 👈 still valid
    )

    # Step 2: Create Celery instance
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
        include=app.config["CELERY_INCLUDE"],
    )

    celery.conf.update(app.config)

    # Step 3: Ensure Flask context is used inside tasks
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
