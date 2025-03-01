""" Módulo para enviar alertas """
import requests
import os
import logging

# Configurar logging estructurado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("notification_slack_service")

# Configuración de Slack
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

def send_slack_alert(message):
    if not SLACK_WEBHOOK_URL:
        logger.warning("Slack Webhook no configurado.")
        return
    
    payload = {"text": message}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
        logger.info("Alerta enviada por Slack.")
    except Exception as e:
        logger.error(f"Error enviando alerta a Slack: {e}")