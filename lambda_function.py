import json
import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    print("Evento recibido:", event)
    for record in event["Records"]:
        try:
            message = json.loads(record["body"])
            send_email(message)
            print(f"Correo enviado a {message['to']}")
        except Exception as e:
            print("Error enviando correo:", str(e))

    return {"statusCode": 200, "body": json.dumps("Correo Enviado Correctamente!")}


def send_email(message):
    try:
        # Configuración del servidor SMTP
        smtp_server = os.environ["SMTP_SERVER"]
        smtp_port = int(os.environ["SMTP_PORT"])
        sender_email = os.environ["SMTP_EMAIL"]
        sender_password = os.environ["SMTP_PASSWORD"]

        # Crear el mensaje
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = message["to"]
        msg["Cc"] = message.get("cc", "")
        msg["Subject"] = "Notificación desde AWS Lambda"

        body = f"Mensaje recibido: {message.get('origen', '')}"
        msg.attach(MIMEText(body, "plain"))

        recipients = [message["to"]]
        if message.get("cc"):
            recipients.append(message["cc"])
        if message.get("bcc"):
            recipients.append(message["bcc"])

        # Enviar el correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, msg.as_string())

        logger.info(f"Correo enviado a {recipients}")

        print("Correo enviado correctamente")

    except Exception as e:
        logger.error(f"Error enviando el correo: {e}")
        print("Error en el envío del correo:", str(e))
        raise
