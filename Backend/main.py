from flask import Flask
from config import Config
from celery_utils import make_celery
from models import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import auth_bp


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

celery = make_celery(app)
db.init_app(app)
JWTManager(app)

print(">>> loading main.py")
print(">>> imported auth_bp")

print("Routes before registering:", auth_bp.deferred_functions)

app.register_blueprint(auth_bp)
print(">>> blueprint registered")

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)