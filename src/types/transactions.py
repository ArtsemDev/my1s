from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic_extra_types.ulid import ULID

__all__ = ["TransactionDTO", "TransactionCreateDTO", "TransactionIntervalStatDTO"]


class TransactionCreateDTO(BaseModel):
    type_id: int = Field(ge=1)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    created_at: date


class TransactionDTO(TransactionCreateDTO):
    user_id: ULID


class TransactionIntervalStatDTO(BaseModel):
    increase: float
    transactions: list[TransactionDTO]
