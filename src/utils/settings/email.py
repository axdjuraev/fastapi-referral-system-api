from pydantic import BaseSettings


class EmailSystemSettings(BaseSettings):
    EMAIL_SENDER: str
    EMAIL_HOST: str
    EMAIL_PORT: str
    EMAIL_SENDER_PASSWD: str
    EMAIL_SEND_TIMOUT: int = 60
