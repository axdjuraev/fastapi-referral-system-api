import logging
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..settings import EmailSystemSettings
from .base import NotificationSystem


class EmailSystem(NotificationSystem):
    def __init__(self, settings: EmailSystemSettings, *, logger: "logging.Logger | None" = None) -> None:
        self.settings = settings
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    async def send(self, receiver: str, content: str, title: str = '', parse_mode: str = 'html'):
        message = MIMEMultipart()
        message['From'] = self.settings.EMAIL_SENDER
        message['To'] = receiver
        message['Subject'] = title
        body = MIMEText(content, parse_mode)
        message.attach(body)

        try:
            await aiosmtplib.send(
                message,
                hostname=self.settings.EMAIL_HOST,
                port=self.settings.EMAIL_PORT,
                username=self.settings.EMAIL_SENDER,
                password=self.settings.EMAIL_SENDER_PASSWD,
                timeout=self.settings.EMAIL_SEND_TIMOUT,
            )
        except Exception as e:
            self.logger.error(e, extra={
                'receiver': receiver,
                'sender': self.settings.EMAIL_SENDER,
                'hostname': self.settings.EMAIL_HOST,
                'port': self.settings.EMAIL_PORT,
                'alert': '\n'.join((
                    f'Error: {e}',
                    f'Receiver: {receiver}',
                    f'Sender: {self.settings.EMAIL_SENDER}',
                    f'Host: {self.settings.EMAIL_HOST}',
                    f'Port: {self.settings.EMAIL_PORT}',
                )),
            })
