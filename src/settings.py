from axsqlalchemy.settings import Settings as DBSettings

from src.utils.settings import JWTSettings, EmailSystemSettings


class Settings(DBSettings, JWTSettings, EmailSystemSettings):
    class Config:
        env_file = '.env'
