from app_logging import celery_logs,normal_logs
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email,To,Content
from celery import shared_task
from flask import current_app
from mutagen import File


me_logger = normal_logs()

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_emails(recipient, subject, text_body=None, html_body=None):
    api_key = current_app.config.get("SENDGRID_API_KEY")
    if not api_key:
        me_logger.warning("SendGrid Api key is missing")
        return "600"

    try:
        from_email = Email(current_app.config["FROM_EMAIL"], current_app.config["FROM_NAME"])
        to_email = To(recipient)
        print("email process still going on")
        # Create mail object (no content yet)
        mail = Mail(from_email=from_email, to_emails=to_email, subject=subject)

        # Always include text version (fallback)
        if text_body:
            mail.add_content(Content("text/plain", text_body))

        # Add HTML version (for clickable link)
        if html_body:
            mail.add_content(Content("text/html", html_body))
        print("email at the verge of finishing")
        sg = SendGridAPIClient(api_key)
        print("Email almost done")
        response = sg.send(mail)
        return "success"
    except Exception as e:
        me_logger.error(f"Failed to send email to {recipient}: {e}")
        return None        


def check_file_validity(audio_id):
    try:
        audio = File(audio_id)
    except Exception as e:
        os.remove(audio_id)
        me_logger.error(f"An error occurred during file validation:{e}")
        return "not_file"
    if audio is None:
        os.remove(audio_id)
        return "not_file"
    try:
        uploads = os.path.join("sharks","upload")
        os.makedirs(uploads,exist_ok=True)
        audio_segment = AudioSegment.from_file(audio_id)
        audio_segment.export(uploads,format="mp3",bitrate="192k")
        os.remove(audio_id)
        return uploads
    except Exception as e:
        os.remove(audio_id)
        me_logger.error(f"Error, audio segment couldn't detect format:{e}")
        return "not_file"



