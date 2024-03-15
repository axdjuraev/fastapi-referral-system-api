import socket
from pydantic import BaseSettings, Field


def get_host_by_name():
    return socket.gethostbyname(socket.gethostname())


class SystemSettings(BaseSettings):
    PORT: int = 8080
    HOST: str = Field(default_factory=get_host_by_name)
