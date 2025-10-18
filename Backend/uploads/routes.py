from . import uploads_bp
from flask import jsonify, request, current_app
import uuid, os, mimetypes
from mutagen import File
from models import AudioStorage, db, User
from app_logging import normal_logs
from tasks import check_file_validity
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from supabase import create_client
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize logger
my_only = normal_logs()

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- UPLOAD AUDIO ---------------- #
@uploads_bp.route("/upload-audio", methods=["POST"])

print("SUPABASE_URL:", SUPABASE_URL is not None)
print("SUPABASE_KEY:", SUPABASE_KEY is not None)
print("supabase type:", type(supabase))
print("has attr 'storage'?:", hasattr(supabase, "storage"))
print("supabase.storage type:", type(getattr(supabase, "storage", None)))
print("dir(supabase)[:40]:", dir(supabase)[:40])
def audio_handling():
    try:
        audios = request.files.getlist("audios")
        preacher = request.form.get("preacher")
        title = request.form.get("title")
        timestamp = request.form.get("date")

        print("FILES:", request.files)
        print("FORM:", request.form)

        # Validate input
        if not preacher or not title or not timestamp or len(audios) == 0:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        upload_folder = current_app.config.get("TEMP_UPLOAD")
        os.makedirs(upload_folder, exist_ok=True)

        success_audios, failed_audios = [], []

        for audio in audios:
            try:
                filename = secure_filename(audio.filename)
                temp_name = f"{uuid.uuid4().hex}_{filename}"
                temp_path = os.path.join(upload_folder, temp_name)
                audio.save(temp_path)

                # Validate/convert file
                converted_path = check_file_validity(temp_path)

                if converted_path != "not_file":
                    mime_type, _ = mimetypes.guess_type(converted_path)
                    mime_type = mime_type or "audio/mpeg"

                    unique_name = f"{uuid.uuid4().hex}.mp3"

                    # Upload to Supabase
                    with open(converted_path, "rb") as f:
                        res = supabase.storage.from_(SUPABASE_BUCKET).upload(unique_name, f)
                        if res.get("error"):
                            raise Exception(res["error"]["message"])

                    # Get public URL (so users can access it directly)
                    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(unique_name)

                    # Save record to database
                    audio_storage = AudioStorage(
                        preacher=preacher,
                        title=title,
                        time_stamp=timestamp,
                        filepath=public_url,
                        original_filename=filename,
                        storage_name=unique_name,
                    )
                    db.session.add(audio_storage)
                    success_audios.append(filename)

                    os.remove(converted_path)

                else:
                    failed_audios.append(filename)
                    os.remove(temp_path)

            except Exception as e:
                my_only.error(f"Error processing {audio.filename}: {e}")
                failed_audios.append(audio.filename)
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        # Commit to DB
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Audios uploaded successfully",
            "uploaded": success_audios,
            "failed": failed_audios
        }), 200

    except Exception as e:
        db.session.rollback()
        my_only.error(f"Upload failed: {e}")
        return jsonify({"status": "error", "message": "Upload failed"}), 500


# ---------------- GET ALL SERMONS ---------------- #
@uploads_bp.route("/get-sermons", methods=["GET"])
def get_sermons():
    print(">>> Inside get_sermons endpoint")

    sermons = (
        db.session.query(
            AudioStorage.id,
            AudioStorage.preacher,
            AudioStorage.title,
            AudioStorage.time_stamp
        )
        .distinct(AudioStorage.id)
        .all()
    )

    print(">>> Retrieved sermons:", sermons)

    sermon_list = [
        {
            "id": sermon.id,
            "pastorName": sermon.preacher,
            "sermonTitle": sermon.title,
            "sermonDate": sermon.time_stamp
        }
        for sermon in sermons
    ]

    return jsonify({"status": "success", "sermons": sermon_list}), 200


# ---------------- GET SERMON AUDIOS ---------------- #
@uploads_bp.route("/get-sermon-audios/<int:sermon_id>", methods=["GET"])
@jwt_required(optional=True)
def get_sermon_audios(sermon_id):
    try:
        sermon_audios = AudioStorage.query.filter_by(id=sermon_id).all()
        if not sermon_audios:
            return jsonify({"status": "error", "message": "No audios found"}), 404

        sermon_data = {
            "id": sermon_id,
            "preacher": sermon_audios[0].preacher,
            "title": sermon_audios[0].title,
            "timestamp": sermon_audios[0].time_stamp,
            "audios": []
        }

        for audio in sermon_audios:
            sermon_data["audios"].append({
                "id": audio.id,
                "name": audio.original_filename,
                "url": audio.filepath  # direct public Supabase link
            })

        return jsonify({"status": "success", "sermon": sermon_data}), 200

    except Exception as e:
        my_only.error(f"Error fetching sermon audios: {e}")
        return jsonify({"status": "error", "message": "Failed to get sermon audios"}), 500
