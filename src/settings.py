from axsqlalchemy.settings import Settings as DBSettings

from src.utils.settings import JWTSettings


class Settings(DBSettings, JWTSettings):
    class Config:
        env_file = '.env'
