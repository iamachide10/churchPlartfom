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

@uploads_bp.route("/upload-audio",methods=["POST"])
def audio_handling():
    audios = request.files.getlist("audios")
    preachers = request.form.getlist("preacher")
    titles = request.form.getlist("title")
    timestamps = request.form.getlist("date")

    if not all([audios,preachers,titles,timestamps]):
        return jsonify({"status":"error","message":"Missing required fields"})

    if not (len(audios) == len(preachers) == len(titles) == len(timestamps)):
        return jsonify({"message":"Mismatched number of audios and details"})

    os.makedirs(current_app.config.get("TEMP_UPLOAD"),exist_ok=True)
    upload_folder = current_app.config.get("TEMP_UPLOAD")

    success_audios = []
    failed_audios = []
    for audio,preacher,title,timestamp in zip(audios,preachers,titles,timestamps):
        filename = secure_filename(audio.filename)
        unique_name = f"{uuid.uuid4().hex}.mp3"
        file_url =  f"audios/{uuid.uuid4().hex}.mp3"      
        file_path = os.path.join(upload_folder,unique_name)
        audio.save(file_path)
        
        status = check_file_validity(file_path)
        if status != "not_file":
            with open(status,"rb") as f:
                s3.upload_fileobj(f,bucket_name,unique_name,ExtraArgs={"ACL":"private","ContentType":status.mimetype})
            audio_storage = AudioStorage(preacher=preacher,title=title,timestamp=timestamp,filepath=file_url,original_filename=filename,storage_name=unique_name)
            db.session.add(audio_storage)
            success_audios.append(filename)
        else:
            failed_audios.append(filename)
    try:
        db.session.commit()
        return jsonify({"success":success_audios,"failed":failed_audios})
    except Exception as e:
        db.session.rollback()
        my_only.error(f"An error occurred {e}")
        return jsonify({"status":"e","message":"Please an error occurred."})
    
        
def generate_presigned_url(filename):
    bucket_name = bucket
    try:
        return supabase.storage.from_(bucket_name).create_signed_url(filename,300)
    except Exception as e:
        my_only({f"An error showed up:{e}"})
        return None 

@uploads_bp.route("/serve-audios/<filename>",methods=["GET"])
@jwt_required()
def bring_audios():
    get_id = get_jwt_identity()
    verify = User.query.filter_by(id=get_id).first()
    if not verify:
        return jsonify({"status":"e","message":"User not  found, please sign up."})
    url = generate_presigned_url(filename)
    if not url:
        return jsonify({"status":"e","message":"File not found or cannot generate URL"})
    return jsonify({"download_url":url})
    

        
            
        
    