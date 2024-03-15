from datetime import datetime
from fastapi.params import Param
from pydantic import parse_obj_as

from src.api.schemas.referral_code import ReferralsSchemas
from src.api.types import TUOW, ActiveUser, MessageSystem, StateAuth, CodeGenerator
from src.api.schemas import ReferralCodeSchemas
from fastapi import APIRouter, HTTPException, Path


router = APIRouter(dependencies=[StateAuth])


@router.get("/", response_model=list[ReferralCodeSchemas])
async def get_all(uow: TUOW):
    """
    Get all referral codes
    """
    return await uow.repo.referral_code.all()


@router.post("/", status_code=201)
async def create(
    expires_at: datetime,
    emailRequest: bool = Param(  # type: ignore
        True,
        description=(
            "возможность получения реферального "
            "кода по email адресу реферера"
        )
    ),
    *,
    uow: TUOW,
    auth: ActiveUser,
    message_system: MessageSystem,
    code_generator: CodeGenerator,
):
    """
    Create referral code
    """
    active_ones = await uow.repo.referral_code.all_active(date=datetime.now())

    if active_ones:
        raise HTTPException(
            status_code=400,
            detail="Found active referral code",
        )

    code = code_generator.generate_referral_code()

    res = await uow.repo.referral_code.add(
        uow.repo.referral_code.Schema(
            code=code,
            user_id=auth.id,
            expires_at=expires_at,
            is_active=True,
        )
    )

    if emailRequest:
        await message_system.send_referral_code(auth.email, code)

    return ReferralCodeSchemas(**res.dict())


@router.delete("/", status_code=200)
async def delete(id: int, uow: TUOW):
    """
    Delete referral code
    """
    await uow.repo.referral_code.delete(id)
    return {"message": "deleted"}


@router.get("/referrals/{id}")
async def get_referrals(*, id: int = Path(..., title='ReferralCodeID'), uow: TUOW):
    """
    Get referrals list by referral-code-id
    """
    referrals = await uow.repo.users.all_by_referral(id)
    return parse_obj_as(list[ReferralsSchemas], referrals)
