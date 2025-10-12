from . import uploads_bp
from flask import jsonify,request,current_app
import uuid,os
from mutagen import File
from models import AudioStorage
from app_logging import normal_logs
from models import db
from tasks import check_file_validity
import boto3
from werkzeug.utils import secure_filename
from dotenv import load_dotenv         
from urllib.parse import urljoin
from flask_jwt_extended import jwt_required,get_jwt_identity
from supabase import create_client
from models import User

my_only = normal_logs()

load_dotenv()

s3 = boto3.client("s3",
        aws_access_key_id=os.getenv("SUPABASE_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("SUPABASE_SECRET_ACCESS_KEY"),                                              
        region_name=os.getenv("REGION_NAME"),                                           
        endpoint_url=os.getenv("ENDPOINT_URL")
        )

bucket_name = os.getenv("SUPABASE_S3_BUCKET")
endpoint = os.getenv("ENDPOINT_URL")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supabase = create_client(supabase_url,supabase_key)


bucket = os.getenv("SUPABASE_S3_BUCKET")

@uploads_bp.route("/upload-audio", methods=["POST"])
def audio_handling():
    # Get multiple audios
    audios = request.files.getlist("audios")

    # These are single values
    preacher = request.form.get("preacher")
    title = request.form.get("title")
    timestamp = request.form.get("date")

    if not all([audios, preacher, title, timestamp]):
        return jsonify({"status": "error", "message": "Missing required fields"})

    os.makedirs(current_app.config.get("TEMP_UPLOAD"), exist_ok=True)
    upload_folder = current_app.config.get("TEMP_UPLOAD")

    success_audios = []
    failed_audios = []

    for audio in audios:
        filename = secure_filename(audio.filename)
        unique_name = f"{uuid.uuid4().hex}.mp3"
        file_url = f"audios/{unique_name}"
        file_path = os.path.join(upload_folder, unique_name)
        audio.save(file_path)

        status = check_file_validity(file_path)
        if status != "not_file":
            with open(status, "rb") as f:
                s3.upload_fileobj(
                    f,
                    bucket_name,
                    unique_name,
                    ExtraArgs={"ACL": "private", "ContentType": status.mimetype},
                )

            audio_storage = AudioStorage(
                preacher=preacher,
                title=title,
                timestamp=timestamp,
                filepath=file_url,
                original_filename=filename,
                storage_name=unique_name,
            )
            db.session.add(audio_storage)
            success_audios.append(filename)
        else:
            failed_audios.append(filename)

    try:
        db.session.commit()
        return jsonify({"success": success_audios, "failed": failed_audios , "message":"audios uploaded"})
    except Exception as e:
        db.session.rollback()
        my_only.error(f"An error occurred {e}")
        return jsonify({"status": "error", "message": "Please an error occurred."})


def generate_presigned_url(filename):
    bucket_name = bucket
    try:
        return supabase.storage.from_(bucket_name).create_signed_url(filename,300)
    except Exception as e:
        my_only({f"An error showed up:{e}"})
        return None 



@uploads_bp.route("/get-sermons", methods=["GET"])
@jwt_required()
def get_sermons():
    user_id = int(get_jwt_identity())
    print(user_id)  
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"status": "e", "message": "User not found"}), 404
    # Group audios by sermon_id (each sermon may have multiple audios)
    sermons = (
        db.session.query(
            AudioStorage.sermon_id,
            AudioStorage.preacher,
            AudioStorage.title,
            AudioStorage.timestamp
        )
        .distinct(AudioStorage.sermon_id)
        .all()
    )

    sermon_list = [
        {
            "id": sermon.sermon_id,
            "pastorName": sermon.preacher,
            "sermonTitle": sermon.title,
            "sermonDate": sermon.timestamp
        }
        for sermon in sermons
    ]

    return jsonify({"status": "success", "sermons": sermon_list})

        
            


@uploads_bp.route("/get-sermon-audios/<int:sermon_id>", methods=["GET"])
@jwt_required()
def get_sermon_audios(sermon_id):
    user_id = int(get_jwt_identity())
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"status": "e", "message": "User not found"}), 404

    sermon_audios = AudioStorage.query.filter_by(sermon_id=sermon_id).all()
    if not sermon_audios:
        return jsonify({"status": "e", "message": "No audios found"}), 404

    sermon_data = {
        "id": sermon_id,
        "preacher": sermon_audios[0].preacher,
        "title": sermon_audios[0].title,
        "timestamp": sermon_audios[0].timestamp,
        "audios": []
    }

    for audio in sermon_audios:
        url = generate_presigned_url(audio.storage_name)
        sermon_data["audios"].append({
            "id": audio.id,
            "name": audio.original_filename,
            "url": url
        })

    return jsonify({"status": "success", "sermon": sermon_data})
