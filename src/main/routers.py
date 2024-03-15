from fastapi import FastAPI

from src import api


def init_routers(app: FastAPI):
    app.include_router(
        api.auth_router,
        prefix="/api/v1/auth",
        tags=["auth"],
    )
    app.include_router(
        api.refferal_code_router,
        prefix="/api/v1/referral-code",
        tags=["referral-code"],
    )
