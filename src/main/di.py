import asyncio
from functools import partial
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from axabc.db.async_uowf import AsyncUOWFactory
from axsqlalchemy.model import Base
from axsqlalchemy.repository.base import AsyncSession
from axsqlalchemy.utils.creation import create_models

from src.db.types import TUOW as DUOW
from src.api import types as api_types
from src.db.repo_collection import RepoCollection
from src.settings import Settings
from src.utils.auth_system import AuthSystem
from src.utils.notification_system import EmailSystem
from src.utils.message_system import MessageSystem
from src.utils.code_generator import SimpleCodeGenerator


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={"msg": "Could not validate credentials"},
    headers={"WWW-Authenticate": "Bearer"},
)


async def auth_dependency(
    uow: api_types.TUOW,
    auth_system: api_types.AuthSystem,
    request: Request,
    token: str = Depends(OAUTH2_SCHEME),
):
    try:
        email = auth_system.get_token_data(token)
    except Exception:
        raise CREDENTIALS_EXCEPTION

    user = await uow.repo.users.get_by_email(email)

    if user is None:
        raise CREDENTIALS_EXCEPTION

    request.state.user = user


def get_active_user(request: Request):
    return request.state.user


async def new_uow(uowf):
    async with uowf() as uow:
        yield uow


async def init_dependencies(app: FastAPI):
    settings = Settings()
    engine = create_async_engine(settings.db_connection_string)
    session_maker = sessionmaker(
        engine,  # type: ignore
        class_=AsyncSession,
        expire_on_commit=False,
    )
    auth_system = AuthSystem(settings)
    email_system = EmailSystem(settings)
    message_system = MessageSystem(email_system)
    code_generator = SimpleCodeGenerator()
    uowf = AsyncUOWFactory(
        repo=RepoCollection,
        session_maker=session_maker,  # type: ignore
    )

    app.dependency_overrides[DUOW] = partial(new_uow, uowf)
    app.dependency_overrides[api_types.TMessageSystem] = lambda: message_system
    app.dependency_overrides[api_types.DepAuthSystem] = lambda: auth_system
    app.dependency_overrides[api_types._EmailSystem] = lambda: email_system
    app.dependency_overrides[api_types._CodeGenerator] = lambda: code_generator
    app.dependency_overrides[api_types.DepStateAuth] = auth_dependency
    app.dependency_overrides[api_types.DepActiveUser] = get_active_user
