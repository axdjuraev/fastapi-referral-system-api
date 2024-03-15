import random
from datetime import datetime

from src.api.types import TUOW, ActiveUser, StateAuth
from src.api.schemas import ReferralCodeSchemas
from fastapi import APIRouter, HTTPException


router = APIRouter(dependencies=[StateAuth])


@router.get("/", response_model=list[ReferralCodeSchemas])
async def get_all(uow: TUOW):
    """
    Get all refferal codes
    """
    return await uow.repo.refferal_code.all()


@router.post("/", status_code=201)
async def create(
    expires_at: datetime,
    *,
    uow: TUOW,
    auth: ActiveUser,
):
    """
    Create refferal code
    """
    active_ones = await uow.repo.refferal_code.all_active(date=datetime.now())

    if active_ones:
        raise HTTPException(
            status_code=400,
            detail="Found active refferal code",
        )

    code = str(random.randint(100000, 999999))

    res = await uow.repo.refferal_code.add(
        uow.repo.refferal_code.Schema(
            code=code,
            user_id=auth.id,
            expires_at=expires_at,
            is_active=True,
        )
    )
    return ReferralCodeSchemas(**res.dict())


@router.delete("/", status_code=204)
async def delete(id: int, uow: TUOW):
    """
    Delete refferal code
    """
    await uow.repo.refferal_code.delete(id)
    return {"message": "deleted"}
