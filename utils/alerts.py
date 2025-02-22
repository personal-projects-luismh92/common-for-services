"""
Alert Notification Module.

This module provides functions for sending alerts via multiple communication channels, including:
- Email (SMTP)
- Slack (Webhook)
- SMS (Twilio)
- Generic Webhook

The module supports structured logging and categorizes alerts by severity levels (INFO, WARNING, CRITICAL).
It is designed to integrate with monitoring and incident response systems.

Dependencies:
    - requests: For making HTTP requests (Slack, Webhooks).
    - smtplib & email.message: For sending emails.
    - twilio.rest.Client: For sending SMS alerts.
    - os: For environment variable configuration.
    - logging: For structured logging of alerts.
    - json: For structured error logging.

Environment Variables:
    - SMTP_SERVER: SMTP server address (default: smtp.gmail.com).
    - SMTP_PORT: SMTP server port (default: 587).
    - SMTP_USER: Email sender address.
    - SMTP_PASSWORD: Password or app-specific password for the SMTP user.
    - SMTP_RECEIVER: Email recipient for alerts.
    - SLACK_WEBHOOK_URL: Webhook URL for sending Slack alerts.
    - TWILIO_ACCOUNT_SID: Twilio account SID for SMS notifications.
    - TWILIO_AUTH_TOKEN: Twilio authentication token.
    - TWILIO_PHONE_NUMBER: Twilio phone number for sending messages.
    - ALERT_PHONE_NUMBER: Recipient phone number for SMS alerts.
    - WEBHOOK_URL: Generic webhook URL for external alerting.

Functions:
    - send_alert_email(subject, body): Sends an email alert.
    - send_slack_alert(message): Sends a Slack notification.
    - send_sms_alert(message): Sends an SMS alert via Twilio.
    - send_webhook_alert(payload): Sends a generic webhook alert.
    - send_alert(subject, message, severity): Sends an alert based on severity.

Usage Example:
    from alert_module import send_alert

    send_alert("Database Connection Failure", "The database server is unreachable.", severity="CRITICAL")
"""

import requests
import smtplib
from email.message import EmailMessage
import os
import logging
import json
from twilio.rest import Client
from enum import Enum

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "monitoring@example.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_password")
EMAIL_RECEIVER = os.getenv("SMTP_RECEIVER", "alerts@example.com")

# Slack Configuration
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
ALERT_PHONE_NUMBER = os.getenv("ALERT_PHONE_NUMBER", "")

# Generic Webhook Configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

# Configure structured logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("monitoring_service")


class AlertSeverity(Enum):
    """Alert Severity Levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

def send_alert_email(subject: str, body: str):
    """Sends an email alert.

    Args:
        subject (str): Email subject.
        body (str): Email body content.

    Logs errors in case of failure.
    """
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
        logger.info("Email alert sent successfully.")
    except Exception as e:
        logger.error(json.dumps({"event": "email_error", "error": str(e)}))


def send_slack_alert(message: str):
    """Sends a Slack alert via webhook.

    Args:
        message (str): Alert message to be sent.

    Logs a warning if Slack is not configured.
    """
    if not SLACK_WEBHOOK_URL:
        logger.warning("Slack Webhook is not configured.")
        return

    payload = {"text": message}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
        logger.info("Slack alert sent successfully.")
    except Exception as e:
        logger.error(f"Error sending Slack alert: {e}")


def send_sms_alert(message: str):
    """Sends an SMS alert using Twilio.

    Args:
        message (str): SMS content.

    Logs a warning if Twilio credentials are not configured.
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logger.warning("Twilio is not configured.")
        return

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=ALERT_PHONE_NUMBER
        )
        logger.info("SMS alert sent successfully.")
    except Exception as e:
        logger.error(f"Error sending SMS: {e}")


def send_webhook_alert(payload: dict):
    """Sends an alert via a generic webhook.

    Args:
        payload (dict): JSON payload containing alert details.

    Logs a warning if the webhook URL is not configured.
    """
    if not WEBHOOK_URL:
        logger.warning("Webhook is not configured.")
        return

    try:
        requests.post(WEBHOOK_URL, json=payload)
        logger.info("Webhook alert sent successfully.")
    except Exception as e:
        logger.error(f"Error sending webhook alert: {e}")



def send_alert(subject: str, message: str, severity: AlertSeverity = AlertSeverity.INFO):
    """Sends an alert based on severity level.

    Args:
        subject (str): Alert subject or title.
        message (str): Alert message content.
        severity (str, optional): Severity level ("INFO", "WARNING", "CRITICAL"). Defaults to "INFO".

    Logs and dispatches the alert through multiple channels.
    """
    logger.info(f"Sending alert ({severity}): {subject}")

    if severity == AlertSeverity.CRITICAL:
        send_alert_email(subject, message)
        send_slack_alert(f"*CRITICAL ALERT*: {message}")
        send_sms_alert(message)
    elif severity == AlertSeverity.WARNING:
        send_alert_email(subject, message)
        send_slack_alert(f"*WARNING ALERT*: {message}")
    elif severity == AlertSeverity.INFO:
        send_slack_alert(f"*INFO ALERT*: {message}")

    send_webhook_alert({"subject": subject, "message": message, "severity": severity})


# Example Usage
if __name__ == "__main__":
    send_alert("Test Alert", "This is a test message", severity=AlertSeverity.CRITICAL)
