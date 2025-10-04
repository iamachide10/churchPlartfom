from . import uploads_bp
from flask import jsonify,request,current_app
import uuid,os
from mutagen import File
from models import AudioStorage,MainAudio
from app_logging import normal_logs
from models import db
from tasks import check_file_validity



my_only = normal_logs()

def get_s3_client():
    return boto3.client("s3",
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

    saved_audios = []
    for audio,preacher,title,timestamp in zip(audios,preachers,titles,timestamps):
        unique_name = f"{uuid.uuid4().hex}.mp3"
        file_path = os.path.join(upload_folder,unique_name)
        audio.save(file_path)

        new_audio = MainAudio(filepath=file_path,filename=unique_name)
        saved_audios.append(new_audio)
        new_details = AudioStorage(preacher=preacher,title=title,time_stamp=timestamp)
        db.session.add(new_audio)
        db.session.add(new_details)
    try:
        failed_audios=[]
        success_audios=[]
        db.session.commit()
        for latest_audio in saved_audios:
            task = check_file_validity(latest_audio.id)
            if task == "none":
                state = "couldn't identify specific audio process"
                failed_audios.append(state)
            elif task == "empty":
                state = "couldn't identify specific audio to process"
            elif task == "notreal":
                state = "Please try uploading a real audio"
            elif task == "fileerror":
                state = "Please an error is in the audio you tried uploading"
            else:
                state = "audio uploaded successfully"
            success_audios.append(latest_audio.id)
            if not task:
                return jsonify({"status":"e","m
        return jsonify({"message":"Audios uploaded successfully","audio_id":audio_id})
    except Exception as e:
        db.session.rollback()
        my_only.error(f"An error occurred during audio uploads:{e}")
        return jsonify({"status":"error","message":"Oops couldn't upload audio, an error occurred"})
