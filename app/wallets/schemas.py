from decimal import Decimal

from pydantic import BaseModel


class WalletCreateSchema(BaseModel):
    title: str
    description: str | None = None


class WalletUpdateSchema(WalletCreateSchema):
    id: int


class WalletSchema(WalletUpdateSchema):
    balance: Decimal
