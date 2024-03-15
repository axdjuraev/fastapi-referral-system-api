from abc import ABC
from typing import Annotated
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from src.db.types import TUOW as _TUOW
from src.db.schemas import OUsers as UserSchemas
from src.utils.depends_stub import Stub
from src.utils.auth_system import AuthSystem


class DepStateAuth(ABC):
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

    def __init__(self, token: str = Depends(OAUTH2_SCHEME)) -> None:
        raise NotImplementedError


class DepAuthSystem(ABC):
    pass


class DepActiveUser(ABC):
    pass


TUOW = Annotated[_TUOW, Depends(Stub(_TUOW))]
StateAuth = Depends(DepStateAuth)
AuthSystem = Annotated[AuthSystem, Depends(Stub(DepAuthSystem))]
ActiveUser = Annotated[UserSchemas, Depends(Stub(DepActiveUser))]
