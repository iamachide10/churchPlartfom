from flask import Flask
from config import Config
from celery_utils import make_celery
from models import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import auth_bp


app = Flask(__name__)
CORS(app,resources={r"/auth/*": {"origins": "http://localhost:8080"}},supports_credentials=True)
app.config.from_object(Config)


celery = make_celery(app)
celery.autodiscover_tasks(["tasks"])
db.init_app(app)
JWTManager(app)

#new commit on backend
print(">>> loading main.py")
print(">>> imported auth_bp")

print("Routes before registering:", auth_bp.deferred_functions)


app.register_blueprint(auth_bp )
# @app.after_request
# def after_request(response):
#     print(">>> Response headers:", dict(response.headers))
#     return response

print(">>> blueprint registered")
for rule in app.url_map.iter_rules():
    print(">>> Route:", rule, "methods:", rule.methods)


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
