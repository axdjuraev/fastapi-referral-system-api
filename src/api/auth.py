from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException
from src.api import schemas
from src.api.types import TUOW, AuthSystem, MessageSystem, CodeGenerator


router = APIRouter()


@router.post("/send-validation-code/{email}", status_code=201)
async def send_validation(
    email: EmailStr,
    message_system: MessageSystem,
    code_generator: CodeGenerator,
    uow: TUOW,
):
    code = code_generator.generate_otp()
    await uow.repo.otp_code.add(
        uow.repo.otp_code.Schema(
            email=email,
            code=code,
        )
    )
    await message_system.send_verification_code(email, code)


@router.post("/register", status_code=201)
async def register(
    otp: str,
    data: schemas.RegistraionSchemas,
    uow: TUOW, auth_system: AuthSystem,
):
    """
    Register user
    """
    code = await uow.repo.otp_code.get_by_code_and_email(otp, data.email)

    if code is None or not code.is_active:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification code",
        )

    if (await uow.repo.users.get_by_email(data.email)) is not None:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )

    referal_code_id = None

    if data.referral_code is not None:
        ref = await uow.repo.referral_code.get_by_code(data.referral_code)

        if ref is None:
            raise HTTPException(
                status_code=400,
                detail="Referral code not found",
            )

        if ref.is_expired():
            raise HTTPException(
                status_code=400,
                detail="Referral code expired",
            )

        referal_code_id = ref.id

    password_hash = auth_system.get_password_hash(data.password)
    await uow.repo.users.add(
        uow.repo.users.Schema(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=password_hash,
            referral_code_id=referal_code_id,
        )
    )

    code.is_active = False
    await uow.repo.otp_code.update(code)

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
