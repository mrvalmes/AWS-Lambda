import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        send_email(message)
    return {
        'statusCode': 200,
        'body': json.dumps('Email enviado Correctamente, by: HV!')
    }

def send_email(message):
    # Configuración del servidor SMTP
    smtp_server = "smtp.gmail.com"  # Cambia según tu proveedor de correo
    smtp_port = 595
    sender_email = "htech220@gmail.com"  # Cambia por tu correo
    sender_password = ""  # Cambia por tu contraseña

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = message['to']
    msg['Cc'] = message.get('cc', '')
    msg['Bcc'] = message.get('bcc', '')
    msg['Subject'] = "Notificación desde AWS Lambda"
    body = f"Mensaje recibido: {message.get('origen', '')}"
    msg.attach(MIMEText(body, 'plain'))

    # Enviar el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
