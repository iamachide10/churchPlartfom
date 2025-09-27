from celery import Celery

def make_celery(app):
    # Step 1: Put Celery settings inside Flask config
    app.config.update(
        CELERY_BROKER_URL="redis://localhost:6379/0",
        CELERY_RESULT_BACKEND="redis://localhost:6379/0",
        CELERY_INCLUDE=["tasks"],  # 👈 must use old-style CELERY_INCLUDE
    )

    # Step 2: Create Celery app using Flask config
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.conf.update(app.config)

    # Step 3: Make sure tasks run inside Flask app context
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
