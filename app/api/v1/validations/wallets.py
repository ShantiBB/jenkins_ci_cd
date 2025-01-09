from decimal import Decimal
from typing import Any

from fastapi.exceptions import HTTPException
from starlette import status


class WalletValidation:

    def validate_exist_obj(obj: Any) -> None:
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Кошелёк не найден!",
            )

    def validate_balance(
        operation_type: str,
        balance: Decimal,
        amount: Decimal,
    ):
        flag = True
        message = None

        if not 10 <= amount <= 10000000:
            message = "Сумма операции должна быть в диапазоне от 10 до 10млн!"
        elif operation_type not in ("deposit", "withdraw"):
            message = "Неверный тип операции!"
        elif operation_type == "withdraw" and balance - amount < 0:
            message = "Недостаточно средств на кошельке!"
        else:
            flag = False

        if flag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message,
            )
