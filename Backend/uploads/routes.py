from . import uploads_bp
from flask import jsonify,request,current_app
import uuid,os
from mutagen import File
from models import AudioStorage,MainAudio

@uploads_bp.route("/upload-audio",methods=["POST"])
def audio_handling():
    audios = request.files.get("audios")
    preacher = request.form.get("preacher")
    title = request.form.get("title")
    timestamp = request.form.get("date")

    if not all([audios,preacher,title,timestamp]):
        return jsonify({"status":"error","message":"Please include audios,title,preacher name and datestamp"})
    for audio in audios:
        unique_name = f"{uuid.uuid4().hex}.mp3"
        os.makedirs(current_app.config.get("AUDIO_UPLOAD"),exist_ok=True)
        upload_folder = current_app.config.get("AUDIO_UPLOAD")
        filepath = os.path.join(upload_folder,unique_name)
        audio.save(filepath)
        real_audio = MainAudio(filepath=filepath,filename=unique_name)
        db.session.add(real_audio)
    try:
        new_audio_details = AudioStorage(preacher=preacher,title=title,time_stamp=timestamp)
        db.session.add(new_audio_details)
        db.session.commit()
        check_file_validity(real_audio.id,filepath)
        return jsonify({"message":"Audio uploaded,validation running in background"})





    


