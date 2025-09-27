from flask import Flask , jsonify
from models import User
from config import Config
import os
from celery_utils import make_celery
from models import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import auth_bp


app = Flask(__name__)
CORS(app,resources={r"/auth/*": {"origins": "https://min-elistarminstry.onrender.com"}},supports_credentials=True)
app.config.from_object(Config)


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
# @app.after_request
# def after_request(response):
#     print(">>> Response headers:", dict(response.headers))
#     return response




print(">>> blueprint registered")
for rule in app.url_map.iter_rules():
    print(">>> Route:", rule, "methods:", rule.methods)


@app.route("/clear-users", methods=["GET"])
def clear_users():
    try:
        num_rows = db.session.query(User).delete()  # delete all users
        db.session.commit()
        return jsonify({"message": f"{num_rows} users deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Welcome to the Church Platform Backend!"


if __name__ == "__main__":
    with app.app_context():
          db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True ,host="0.0.0.0", port=port)

