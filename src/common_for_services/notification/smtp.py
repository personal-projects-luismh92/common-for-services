""" Módulo para enviar alertas """
import smtplib
from email.message import EmailMessage
import os
import logging
import json


# Configuración de correo
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "monitoring@example.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_password")
EMAIL_RECEIVER = os.getenv("SMTP_RECEIVER", "alerts@example.com") 

# Configurar logging estructurado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("notification_smtp_service")


def send_alert_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        logger.error(json.dumps({"event": "email_error", "error": str(e)}))