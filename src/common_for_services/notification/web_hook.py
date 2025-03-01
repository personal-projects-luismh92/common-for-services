""" Módulo para enviar alertas  por webhook"""
import requests
import os
import logging

# Configurar logging estructurado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("notification_webhook_service")

# Configuración de Webhook genérico
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

def send_webhook_alert(payload):
    if not WEBHOOK_URL:
        logger.warning("Webhook no configurado.")
        return
    
    try:
        requests.post(WEBHOOK_URL, json=payload)
        logger.info("Alerta enviada por Webhook.")
    except Exception as e:
        logger.error(f"Error enviando alerta por Webhook: {e}")