""" Módulo para enviar alertas """
import smtplib
from email.message import EmailMessage
import os
import logging

# Configurar logging estructurado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("notification_smtp_service")

class EmailService:
    """Handles sending email notifications."""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_username = os.getenv("SMTP_USERNAME", "aplication_email@gmail.com")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "your_email_password")
        self.admin_email = os.getenv("ADMIN_EMAIL", "admin_role@example.com")

    def send_email(self, subject: str, body: str):
        """Sends an email with the given subject and body."""
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg["From"] = self.smtp_username
            msg["To"] = self.admin_email
            msg["Subject"] = subject

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.smtp_username, self.admin_email, msg.as_string())

            logger.info(f"Error email sent to {self.admin_email}")

        except Exception as e:
            logger.critical(f"Failed to send error email: {e}")