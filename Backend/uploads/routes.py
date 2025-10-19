from . import uploads_bp
from flask import jsonify, request, current_app
import uuid, os, mimetypes
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from supabase import create_client, Client
from flask_jwt_extended import jwt_required
from app_logging import normal_logs
from tasks import check_file_validity

# Initialize logger
my_only = normal_logs()

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
@uploads_bp.route("/get-signed-urls", methods=["POST"])
def get_signed_urls():
    try:
        # Generate unique sermon ID
        sermon_id = f"SERMON-{uuid.uuid4().hex[:8]}"

        # Extract data from request
        filenames = request.form.getlist("filenames")
        preacher = request.form.get("preacher")
        title = request.form.get("title")
        timestamp = request.form.get("date")

        # Validate required fields
        if not preacher or not title or not timestamp or len(filenames) == 0:
            return jsonify({
                "status": "error",
                "message": "Missing required fields"
            }), 400

        # Initialize Supabase bucket
        bucket = supabase.storage.from_(SUPABASE_BUCKET)

        signed_urls = []
        for filename in filenames:
            safe_name = secure_filename(filename)
            supabase_path = f"sermons/{sermon_id}/{safe_name}"

            # ✅ Create signed URL for upload
            signed_url_data = bucket.create_signed_upload_url(supabase_path)

            # Some SDK versions return dicts, others return objects
            signed_url = signed_url_data.get("signed_url") if isinstance(signed_url_data, dict) else signed_url_data.signed_url

            signed_urls.append({
                "filename": safe_name,
                "upload_url": signed_url,
                "supabase_path": supabase_path
            })

        # ✅ Respond with metadata + URLs
        return jsonify({
            "status": "success",
            "sermon_id": sermon_id,
            "urls": signed_urls,
            "preacher": preacher,
            "title": title,
            "timestamp": timestamp
        }), 200

    except Exception as e:
        # In case anything breaks
        current_app.logger.error(f"Error generating signed URLs: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to generate signed URLs"
        }), 500

@uploads_bp.route("/register-sermon", methods=["POST"])
def register_sermon():
    try:
        data = request.get_json()

        sermon_id = data.get("sermon_id")
        preacher = data.get("preacher")
        title = data.get("title")
        timestamp = data.get("timestamp")
        audios = data.get("audios", [])

        if not sermon_id or not preacher or not title or not timestamp or not audios:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        for audio in audios:
            supabase_path = audio.get("supabase_path")
            filename = audio.get("filename")

            public_url = (
                f"{SUPABASE_URL}/storage/v1/object/public/"
                f"{SUPABASE_BUCKET}/{supabase_path}"
            )

            # Save metadata to your Supabase table
            supabase.table("audio_storage").insert({
                "sermon_id": sermon_id,
                "preacher": preacher,
                "title": title,
                "timestamp": timestamp,
                "original_filename": filename,
                "file_path": public_url,
                "storage_name": supabase_path,
            }).execute()

        return jsonify({
            "status": "success",
            "message": "Sermon registered successfully",
            "sermon_id": sermon_id
        }), 200

    except Exception as e:
         my_only.error(f"Error registring sermons: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to register sermon"
        }), 500



# ---------------- UPLOAD AUDIO ---------------- #
@uploads_bp.route("/upload-audio", methods=["POST"])
def audio_handling():
    try:
        audios = request.files.getlist("audios")
        preacher = request.form.get("preacher")
        title = request.form.get("title")
        timestamp = request.form.get("date")
        sermon_id = f"SERMON-{uuid.uuid4().hex[:8]}"

        # Validate inputs
        if not preacher or not title or not timestamp or len(audios) == 0:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        upload_folder = current_app.config.get("TEMP_UPLOAD", "./temp_uploads")
        os.makedirs(upload_folder, exist_ok=True)

        success_audios, failed_audios = [], []

        # Initialize storage client and bucket once
        storage_client = supabase.storage  # ✅ no parentheses
        bucket = storage_client.from_(SUPABASE_BUCKET)

        # Upload each audio file
        for audio in audios:
            try:
                filename = secure_filename(audio.filename)
                temp_name = f"{uuid.uuid4().hex}_{filename}"
                temp_path = os.path.join(upload_folder, temp_name)
                audio.save(temp_path)

                converted_path = check_file_validity(temp_path)

                if converted_path != "not_file":
                    unique_name = f"{sermon_id}_{uuid.uuid4().hex}_{filename}"
                    supabase_path = f"sermons/{sermon_id}/{unique_name}"

                    # Upload to Supabase
                    with open(converted_path, "rb") as f:
                        bucket.upload(supabase_path, f)

                    # Get public URL
                    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{supabase_path}"

                    # Save record to Supabase table
                    audio_data = {
                        "sermon_id": sermon_id,
                        "preacher": preacher,
                        "title": title,
                        "timestamp": timestamp,
                        "original_filename": filename,
                        "file_path": public_url,
                        "storage_name": unique_name,
                    }
                    supabase.table("audio_storage").insert(audio_data).execute()
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
            "sermon_id": sermon_id,
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
        response = supabase.table("audio_storage").select("*").execute()
        records = response.data or []

        if not records:
            return jsonify({"status": "error", "message": "No sermons found"}), 404

        unique_sermons = {}
        for record in records:
            sermon_id = record.get("sermon_id")
            if sermon_id not in unique_sermons:
                unique_sermons[sermon_id] = {
                    "sermon_id": sermon_id,
                    "pastorName": record.get("preacher"),
                    "sermonTitle": record.get("title"),
                    "sermonDate": record.get("timestamp"),
                }

        return jsonify({
            "status": "success",
            "sermons": list(unique_sermons.values())
        }), 200

    except Exception as e:
        my_only.error(f"Error fetching sermons: {e}")
        return jsonify({"status": "error", "message": "Failed to get sermons"}), 500


# ---------------- GET SERMON AUDIOS ---------------- #
@uploads_bp.route("/get-sermon-audios/<string:sermon_id>", methods=["GET"])
@jwt_required(optional=True)
def get_sermon_audios(sermon_id):
    try:
        response = supabase.table("audio_storage").select("*").eq("sermon_id", sermon_id).execute()
        records = response.data or []

        if not records:
            return jsonify({"status": "error", "message": "No audios found for this sermon"}), 404

        sample = records[0]
        sermon_data = {
            "sermon_id": sample.get("sermon_id"),
            "title": sample.get("title"),
            "preacher": sample.get("preacher"),
            "timestamp": sample.get("timestamp"),
            "audios": [
                {"name": record.get("original_filename"), "url": record.get("file_path")}
                for record in records
            ]
        }

        return jsonify({"status": "success", "sermon": sermon_data}), 200

    except Exception as e:
        my_only.error(f"Error fetching sermon audios: {e}")
        return jsonify({"status": "error", "message": "Failed to get sermon audios"}), 500
