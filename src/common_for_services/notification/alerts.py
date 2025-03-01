""" Módulo para enviar alertas """
import logging
from common_for_services.notification.smtp import send_alert_email
from common_for_services.notification.sms_twilio import send_sms_alert
from common_for_services.notification.slack import send_slack_alert
from common_for_services.notification.web_hook import send_webhook_alert


# Configurar logging estructurado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("notification__service")

def send_alert(subject, message, severity="INFO"):
    logger.info(f"Enviando alerta ({severity}): {subject}")
    
    if severity == "CRITICAL":
        send_alert_email(subject, message)
        send_slack_alert(f"*CRITICAL ALERT*: {message}")
        send_sms_alert(message)
    elif severity == "WARNING":
        send_alert_email(subject, message)
        send_slack_alert(f"*WARNING ALERT*: {message}")
    elif severity == "INFO":
        send_slack_alert(f"*INFO ALERT*: {message}")
    
    send_webhook_alert({"subject": subject, "message": message, "severity": severity})

# Ejemplo de uso:
if __name__ == "__main__":
    send_alert("Test de Alerta", "Este es un mensaje de prueba", severity="CRITICAL")