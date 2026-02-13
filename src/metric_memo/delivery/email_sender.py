from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from src.metric_memo.config.settings import SmtpSettings


class EmailSender:
    def __init__(self, smtp_settings: SmtpSettings):
        self.smtp_settings = smtp_settings

    def send_html(self, recipients: list[str], subject: str, html_body: str):
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = f"{self.smtp_settings.from_name} <{self.smtp_settings.user}>"
        msg.attach(MIMEText(html_body, "html"))

        port = self.smtp_settings.port or (
            465
            if self.smtp_settings.use_ssl
            else 587 if self.smtp_settings.use_starttls else 25
        )

        if self.smtp_settings.use_ssl:
            server = smtplib.SMTP_SSL(self.smtp_settings.host, port)
        else:
            server = smtplib.SMTP(self.smtp_settings.host, port)

        with server:
            if self.smtp_settings.use_starttls:
                server.starttls()

            if self.smtp_settings.user and self.smtp_settings.password:
                server.login(self.smtp_settings.user, self.smtp_settings.password)

            for recipient in recipients:
                msg["To"] = recipient
                server.send_message(msg)
