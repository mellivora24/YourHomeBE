import smtplib
from email.mime.text import MIMEText
from config.settings import settings

class EmailService:
    def __init__(self):
        self.sender_email = "yourhome.admin@gmail.com"
        self.sender_password = "12345678"

    async def send_email(self, receiver_email: str, subject: str, content: str):
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = receiver_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)

email_service = EmailService()