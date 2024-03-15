from fastapi import APIRouter, Depends, HTTPException
from src.api import schemas
from src.api.types import TUOW, AuthSystem


router = APIRouter()


@router.post("/", status_code=201)
async def register(data: schemas.RegistraionSchemas, uow: TUOW, auth_system: AuthSystem):
    """
    Register user
    """
    if (await uow.repo.users.get_by_email(data.email)) is not None:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )

    password_hash = auth_system.get_password_hash(data.password)

    await uow.repo.users.add(
        uow.repo.users.Schema(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=password_hash,
        )
    )
    return {"message": "register"}


@router.post("/login")
async def login(
    uow: TUOW,
    auth_system: AuthSystem,
    data: schemas.LoginSchemas = Depends(),
):
    """
    Login user
    """
    user = await uow.repo.users.get_by_email(data.username)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User with this email not found",
        )

    if not auth_system.varify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )

    return schemas.LoginPayloadSchema(
        user=schemas.LoginInfoSchemas.from_orm(user),
        access_token=auth_system.create_access_token(user.email),
        refresh_token=auth_system.create_refresh_token(user.email),
    )
