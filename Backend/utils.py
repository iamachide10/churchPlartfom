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
        
@shared_task(bind=True,max_retries=4,default_retry_delay=10)
def check_file_validity(self,filepath):
      try:
            audio = File(filepath)
            

