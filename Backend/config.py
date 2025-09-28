import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # Render/Postgres will inject this
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "access_cookie"
    JWT_REFRESH_COOKIE_NAME = "refresh_cookie"
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_COOKIE_SAMESITE = None
    SECRET_KEY = os.getenv("SECRET_KEY")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    FROM_NAME = os.getenv("FROM_NAME")
    JWT_COOKIE_HTTPONLY = True
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_REFRESH_COOKIE_PATH = "/refresh-tokens"
    broker_url = os.getenv("broker_url")
    result_backend = os.getenv("result_backend")
    AUDIO_UPLOAD = os.path.join(BASE_DIR, "shark", "audios")
    TEMP_UPLOAD = os.path.join(BASE_DIR, "temp", "uploads")
