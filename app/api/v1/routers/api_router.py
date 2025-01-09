from fastapi import APIRouter

from .wallets import router as wallet_router

router = APIRouter(
    prefix="/api/v1",
)


router.include_router(wallet_router)
