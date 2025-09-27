from . import uploads_bp
from flask import jsonify,request,current_app
import uuid,os
from mutagen import File
from models import AudioStorage,MainAudio
from app_logging import normal_logs
from models import db
from tasks import check_file_validity
from main import celery
from celery.result import AsyncResult

my_only = normal_logs()

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
        audio_id=[]
        task_id_list=[]
        db.session.commit()
        for latest_audio in saved_audios:
            task = check_file_validity.delay(latest_audio.id)
            audio_id.append(latest_audio.id)
            task_id_list.append(task.id)
        return jsonify({"message":"Audios uploaded validation are still going on at the background","task_id":task_id_list,"audio_id":audio_id})
    except Exception as e:
        db.session.rollback()
        my_only.error(f"An error occurred during audio uploads:{e}")
        return jsonify({"status":"error","message":"Oops couldn't upload audio, an error occurred"})

@uploads_bp.route("/task-status/<task_id>")
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
