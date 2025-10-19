from . import uploads_bp
from flask import jsonify, request, current_app
import uuid, os, mimetypes
from mutagen import File
from app_logging import normal_logs
from tasks import check_file_validity
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from supabase import create_client, Client
from flask_jwt_extended import jwt_required

# Initialize logger
my_only = normal_logs()

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- UPLOAD AUDIO ---------------- #
@uploads_bp.route("/upload-audio", methods=["POST"])
def audio_handling():
    print("SUPABASE_URL:", bool(SUPABASE_URL))
    print("SUPABASE_KEY:", bool(SUPABASE_KEY))
    print("supabase type:", type(supabase))
    print("🔍 SUPABASE_URL =", SUPABASE_URL)
    print("🔍 SUPABASE_KEY=", SUPABASE_KEY)
    print("🔍 SUPABASE_Name=", SUPABASE_BUCKET)

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

                # Validate or convert file
                converted_path = check_file_validity(temp_path)

                if converted_path != "not_file":
                    mime_type, _ = mimetypes.guess_type(converted_path)
                    mime_type = mime_type or "audio/mpeg"
                    unique_name = f"{uuid.uuid4().hex}_{filename}"

                    # ✅ Upload to Supabase
                    with open(converted_path, "rb") as f:
                        supabase.storage().from_(SUPABASE_BUCKET).upload(unique_name, f)

                    # ✅ Get public URL
                    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{unique_name}"

                    # ✅ Save record directly to Supabase table
                    data = {
                        "preacher": preacher,
                        "title": title,
                        "timestamp": timestamp,
                        "original_filename": filename,
                        "file_path": public_url,
                        "storage_name": unique_name
                    }

                    supabase.table("audio_storage").insert(data).execute()

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

        return jsonify({
            "status": "success",
            "message": "Audios uploaded successfully",
            "uploaded": success_audios,
            "failed": failed_audios
        }), 200

    except Exception as e:
        my_only.error(f"Upload failed: {e}")
        return jsonify({"status": "error", "message": "Upload failed"}), 500


# ---------------- GET ALL SERMONS ---------------- #
@uploads_bp.route("/get-sermons", methods=["GET"])
def get_sermons():
    try:
        # Fetch all sermon records from Supabase
        response = supabase.table("audio_storage").select("*").execute()
        records = response.data or []

        if not records:
            return jsonify({"status": "error", "message": "No sermons found"}), 404

        # Use a dictionary to ensure only one entry per sermon title
        unique_sermons = {}
        for record in records:
            title = record.get("title")
            if title not in unique_sermons:
                unique_sermons[title] = {
                    "id": record.get("id"),
                    "pastorName": record.get("preacher"),
                    "sermonTitle": record.get("title"),
                    "sermonDate": record.get("timestamp")
                }

        # Convert dictionary values to a list
        sermons = list(unique_sermons.values())

        return jsonify({
            "status": "success",
            "sermons": sermons
        }), 200

    except Exception as e:
        my_only.error(f"Error fetching sermons: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to get sermons"
        }), 500


# ---------------- GET SERMON AUDIOS ---------------- #
@uploads_bp.route("/get-sermon-audios/<int:sermon_id>", methods=["GET"])
@jwt_required(optional=True)
def get_sermon_audios(sermon_id):
    try:
        response = supabase.table("audio_storage").select("*").eq("id", sermon_id).execute()
        records = response.data or []

        if not records:
            return jsonify({"status": "error", "message": "No audios found"}), 404

        record = records[0]

        sermon_data = {
            "id": record.get("id"),
            "preacher": record.get("preacher"),
            "title": record.get("title"),
            "timestamp": record.get("timestamp"),
            "audios": [
                {
                    "name": record.get("original_filename"),
                    "url": record.get("filepath")
                }
            ]
        }

        return jsonify({"status": "success", "sermon": sermon_data}), 200

    except Exception as e:
        my_only.error(f"Error fetching sermon audios: {e}")
        return jsonify({"status": "error", "message": "Failed to get sermon audios"}), 500
