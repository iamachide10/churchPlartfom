from app_logging import celery_logs
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email,To,Content
from celery import shared_task
from flask import current_app
from mutagen import File

logger = celery_logs()

@shared_task(bind=True,max_retries=3,default_retry_delay=10)
def send_emails(self,recipient,subject,body):
        api_key = current_app.config.get("SENDGRID_API_KEY")
        if not api_key:
              logger.warning("SendGrid Api key is missing")
              raise self.retry(exc=ValueError("Missing SendGrid Api key"))
        try:
            sg = SendGridAPIClient(api_key=current_app.config["SENDGRID_API_KEY"])
            from_email = Email(current_app.config["FROM_EMAIL"],current_app.config["FROM_NAME"])
            to_email = To(recipient)
            content = Content("text/plain",body)
            mail = Mail(from_email,to_email,subject,content)

            response = sg.send(mail) 
            logger.info(f"Email sent to {recipient}, status {response.status_code}")
            return response.status_code
        except Exception as e:
              logger.error(f"Failed to send email to {recipient}: {e}")
              raise self.retry(exc=e)



@shared_task
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


