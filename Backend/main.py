from flask import Flask , jsonify
from models import User
from config import Config
import os
from celery_utils import make_celery
from models import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import auth_bp
from uploads import uploads_bp  
from celery.result import AsyncResult
from flask_migrate import Migrate
from models import AudioStorage

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["https://min-elistarminstry.onrender.com"])

app.config.from_object(Config)

migrate = Migrate(app, db)
celery = make_celery(app)
celery.autodiscover_tasks(["tasks"])
db.init_app(app)
JWTManager(app)

#new commit on backend
print(">>> loading main.py")
print(">>> imported auth_bp")

print("Routes before registering:", auth_bp.deferred_functions)


app.register_blueprint(auth_bp)
app.register_blueprint(uploads_bp)

data=AudioStorage.query.all()
print(">>> AudioStorage records:", data)

# @app.after_request
# def after_request(response):
#     print(">>> Response headers:", dict(response.headers))
#     return response




print(">>> blueprint registered")
for rule in app.url_map.iter_rules():
    print(">>> Route:", rule, "methods:", rule.methods)



@app.route("/")
def home():
    return "Welcome to the Church Platform Backend!"


@app.route("/task-status/<task_id>")
def task_status(task_id):
    result = AsyncResult(task_id, app=celery)
    if result.state == "PENDING":
        return {"state": result.state, "message": "Task is still waiting in the queue..."}
    elif result.state == "STARTED":
        return {"state": result.state, "message": "Task is currently running..."}
    elif result.state == "SUCCESS":
        return {"state": result.state, "result": result.result}
    elif result.state == "FAILURE":
        return {"state": result.state, "reason": str(result.info)}
    else:
        return {"state": result.state, "message": "Unknown state"}


if __name__ == "__main__":
    with app.app_context():
          db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True ,host="0.0.0.0", port=port)

