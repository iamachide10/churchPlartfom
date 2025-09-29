from app_logging import celery_logs,normal_logs
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email,To,Content
from celery import shared_task
from flask import current_app
from mutagen import File

logger = celery_logs()
me_logger = normal_logs()

def send_emails(recipient,subject,body):
        api_key = current_app.config.get("SENDGRID_API_KEY")
        if not api_key:
              me_logger.warning("SendGrid Api key is missing")
              return "600"
        try:
            sg = SendGridAPIClient(api_key=current_app.config["SENDGRID_API_KEY"])
            from_email = Email(current_app.config["FROM_EMAIL"],current_app.config["FROM_NAME"])
            to_email = To(recipient)
            content = Content("text/plain",body)
            mail = Mail(from_email,to_email,subject,content)

            response = sg.send(mail) 
            return "success"
        except Exception as e:
              me_logger.error(f"Failed to send email to {recipient}: {e}")
              return None


def check_file_validity(audio_id):
    check = MainAudio.query.filter_by(id=audio_id).first()
    if not check:
        raise Exception("Couldn't process specific audio")
    verify = AudioStorage.query.filter_by(id=check.id).first()
    if not verify:
        return Exception("Couldn't process specific audio")
    filepath = check.filepath
    try:
        audio = File(filepath)
    except Exception as e:
        os.remove(filepath)
        db.session.delete(check)
        db.session.delete(verify)
        db.session.commit()
        logger.error(f"An error occurred during file validation:{e}")
        return {"message":"Please try uploading a real audio"}
    if audio is None:
        os.remove(filepath)
        db.session.delete(check)
        db.session.delete(verify)
        db.session.commit()
        raise Exception("Please upload a real audio")
    os.makedirs(current_app.config.get("AUDIO_UPLOAD"),exist_ok=True)
    export_path = os.path.join(current_app.config.get("AUDIO_UPLOAD"),check.filename)
    try:
        audio_segment = AudioSegment.from_file(filepath)
        audio_segment.export(export_path,format="mp3",bitrate="192k")
        os.remove(filepath)
        return {"message":f"Audio saved successfully"}
    except Exception as e:
        os.remove(filepath)
        db.session.delete(check)
        db.session.delete(verify)
        db.session.commit()
        logger.error(f"Error, audio segment couldn't detect format:{e}")
        return {"message":"Audio is corrupted"}


