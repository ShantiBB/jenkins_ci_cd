from decimal import Decimal

from fastapi import APIRouter

from app.api.v1.validations.wallets import WalletValidation
from app.core.database.db_helper import AsyncSessionDep
from app.wallets.dao import WalletDAO
from app.wallets.schemas import WalletCreateSchema, WalletSchema

router = APIRouter(
    prefix="/wallets",
    tags=["Кошелёк"],
)


@router.post("/")
async def create_wallet(
    session: AsyncSessionDep,
    data: WalletCreateSchema,
) -> WalletSchema:
    return await WalletDAO.create(
        session=session,
        **data.model_dump(),
    )


@router.get("/")
async def get_all_wallets(
    session: AsyncSessionDep,
) -> list[WalletSchema]:
    return await WalletDAO.get_all(session)


@router.get("/{wallet_id}/")
async def get_wallet_by_id(
    wallet_id: int,
    session: AsyncSessionDep,
) -> WalletSchema:
    wallet = await WalletDAO.get_by_id(
        obj_id=wallet_id,
        session=session,
    )
    WalletValidation.validate_exist_obj(wallet)
    return wallet


@router.put("/{wallet_id}/")
async def update_wallet(
    wallet_id: int,
    session: AsyncSessionDep,
    data: WalletCreateSchema,
) -> str:
    res = await WalletDAO.update(
        obj_id=wallet_id,
        session=session,
        **data.model_dump(),
    )
    WalletValidation.validate_exist_obj(res)
    return "Кошелёк успешно изменён"


@router.delete("/{wallet_id}/")
async def delete_wallet(
    wallet_id: int,
    session: AsyncSessionDep,
) -> str:
    res = await WalletDAO.delete(
        obj_id=wallet_id,
        session=session,
    )
    WalletValidation.validate_exist_obj(res)
    return "Кошелёк успешно удалён"


@router.post("/{wallet_id}/operation/")
async def update_wallet_balance(
    wallet_id: int,
    operation_type: str,
    amount: Decimal,
    session: AsyncSessionDep,
) -> str:
    balance = await WalletDAO.get_balance(
        wallet_id=wallet_id,
        session=session,
    )

    WalletValidation.validate_exist_obj(balance)
    WalletValidation.validate_balance(
        operation_type=operation_type,
        balance=balance,
        amount=amount,
    )

    await WalletDAO.update_balance(
        wallet_id=wallet_id,
        operation_type=operation_type,
        balance=balance,
        amount=amount,
        session=session,
    )
    return "Транзакция прошла успешно!"
