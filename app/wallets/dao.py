from decimal import Decimal

from sqlalchemy import select, update

from app.core.dao import BaseModelDAO
from app.core.database.db_helper import AsyncSessionDep
from app.core.database.models.wallets import Wallet


class WalletDAO(BaseModelDAO):
    model = Wallet

    @classmethod
    async def get_balance(
        cls,
        wallet_id: int,
        session: AsyncSessionDep,
    ) -> Decimal | None:
        query = select(cls.model.balance).filter_by(id=wallet_id)
        res = await session.scalars(query)
        balance = res.one_or_none()
        return balance

    @classmethod
    async def update_balance(
        cls,
        wallet_id: int,
        operation_type: str,
        balance: Decimal,
        amount: Decimal,
        session: AsyncSessionDep,
    ) -> None:
        if operation_type == "deposit":
            balance += amount
        else:
            balance -= amount

        stmt = (
            update(cls.model)
            .filter_by(id=wallet_id)
            .values(balance=balance)
        )
        await session.execute(stmt)
        await session.commit()
