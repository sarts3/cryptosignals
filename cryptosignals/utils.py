import os, smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, message):
    sender_email = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_SENDER_PASS')
    receiver_email = os.getenv('EMAIL_RECEIVER')

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html = f"""\
    <html>
    <body>
        {message}
    </body>
    </html>
    """
    part = MIMEText(html, "html")
    msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
