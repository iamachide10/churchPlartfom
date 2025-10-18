from app_logging import celery_logs,normal_logs
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email,To,Content, TrackingSettings, ClickTracking,From
from celery import shared_task
from flask import current_app
from mutagen import File
import os
from pydub import AudioSegment
import time
import mimetypes, uuid




me_logger = normal_logs()

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content



def send_emails(recipient, subject, body):
    sg = SendGridAPIClient(api_key = current_app.config.get("SENDGRID_API_KEY"))
    if not isinstance(subject, str):
        subject = str(subject)

    from_email = From(current_app.config["FROM_EMAIL"], current_app.config["FROM_NAME"])
    print(f"✅ DEBUG subject: {subject} ({type(subject)})")

    mail = Mail(
        from_email=from_email,
        to_emails=To(recipient),
        subject=subject
    )
    mail.add_content(Content("text/plain", str(body)))  # force body to string

    tracking_settings = TrackingSettings()
    tracking_settings.click_tracking = ClickTracking(enable=False, enable_text=False)
    mail.tracking_settings = tracking_settings
    try:
        response = sg.send(mail)
        print(f"📨 Email sent, status code: {response.status_code}")
        return response.status_code
    except Exception as e:
        me_logger.error(f"Failed to send email to {recipient}: {e}")
        print(f"❌ Error sending email: {e}")
        return None


# def send_emails(recipient, subject, text_body=None, html_body=None):
#     api_key = current_app.config.get("SENDGRID_API_KEY")
#     if not api_key:
#         me_logger.warning("SendGrid Api key is missing")
#         return "600"

#     try:
#         from_email = Email(current_app.config["FROM_EMAIL"], current_app.config["FROM_NAME"])
#         to_email = To(recipient)
#         print("email process still going on")
#         # Create mail object (no content yet)
#         mail = Mail(from_email=from_email, to_emails=to_email, subject=subject)

#         # Always include text version (fallback)
#         if text_body:
#             mail.add_content(Content("text/plain", text_body))

#         # Add HTML version (for clickable link)
#         if html_body:
#             mail.add_content(Content("text/html", html_body))
#         print("email at the verge of finishing")tasks.py#         sg = SendGridAPIClient(api_key)
#         print("Email almost done")
#         response = sg.send(mail)
#         return "success"
#     except Exception as e:
#         me_logger.error(f"Failed to send email to {recipient}: {e}")
#         return None        







def check_file_validity(audio_path):
    try:
        uploads = os.path.join("sharks", "upload")
        os.makedirs(uploads, exist_ok=True)

        # 🔍 Try to detect the file's MIME type automatically
        mime_type, _ = mimetypes.guess_type(audio_path)
        file_ext = os.path.splitext(audio_path)[1].lower().replace(".", "")

        # ✅ Let ffmpeg auto-detect if unsure
        try:
            audio_segment = AudioSegment.from_file(audio_path)
        except Exception as e1:
            # Retry with extension-based format if ffmpeg fails to auto-detect
            try:
                audio_segment = AudioSegment.from_file(audio_path, format=file_ext)
            except Exception as e2:
                print(f"Both auto-detect and manual format detection failed: {e2}")
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                return "not_file"

        # 🎧 Export to MP3
        output_path = os.path.join(uploads, f"{uuid.uuid4()}.mp3")
        audio_segment.export(output_path, format="mp3", bitrate="192k")

        # 🧹 Clean up original file
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return output_path

    except Exception as e:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        print(f"Error processing audio file: {e}")
        return "not_file"

