from abc import ABC
from typing import Annotated
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from src.db.types import TUOW as _TUOW
from src.db.schemas import OUsers as UserSchemas
from src.utils.depends_stub import Stub
from src.utils.auth_system import AuthSystem
from src.utils.message_system import MessageSystem as TMessageSystem
from src.utils.code_generator import CodeGenerator as _CodeGenerator
from src.utils.notification_system import EmailSystem as _EmailSystem


class DepStateAuth(ABC):
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

    def __init__(self, token: str = Depends(OAUTH2_SCHEME)) -> None:
        raise NotImplementedError


class DepAuthSystem(ABC):
    pass


class DepActiveUser(ABC):
    pass


class DepMessageSystem(ABC):
    pass


TUOW = Annotated[_TUOW, Depends(Stub(_TUOW))]
StateAuth = Depends(DepStateAuth)
AuthSystem = Annotated[AuthSystem, Depends(Stub(DepAuthSystem))]
MessageSystem = Annotated[TMessageSystem, Depends(Stub(TMessageSystem))]
ActiveUser = Annotated[UserSchemas, Depends(Stub(DepActiveUser))]
EmailSystem = Annotated[_EmailSystem, Depends(Stub(_EmailSystem))]
CodeGenerator = Annotated[_CodeGenerator, Depends(Stub(_CodeGenerator))]
