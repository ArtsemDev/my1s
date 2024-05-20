from datetime import date

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from starlette.requests import Request

from src.dependencies import AsyncDBSession, Authenticate
from src.types.transactions import TransactionDTO, TransactionCreateDTO, TransactionIntervalStatDTO
from src.models.models import Transaction, TransactionType

router = APIRouter(dependencies=[Authenticate])


@router.post(path="/transactions", response_model=TransactionDTO, status_code=201)
async def create_transaction(request: Request, db_session: AsyncDBSession, data: TransactionCreateDTO):
    transaction = Transaction(**data.model_dump(), user_id=request.scope["state"]["user"].id)
    db_session.add(instance=transaction)
    try:
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400)
    else:
        await db_session.refresh(instance=transaction)
        return TransactionDTO.model_validate(obj=transaction, from_attributes=True)


@router.get(path="/transactions", response_model=TransactionIntervalStatDTO, status_code=200)
async def transactions_list(
        db_session: AsyncDBSession,
        date_from: date = Query(default=..., alias="dateFrom"),
        date_to: date = Query(default=..., alias="dateTo"),
):
    if date_from >= date_to:
        raise HTTPException(status_code=422)

    objs = await db_session.scalars(
        statement=select(Transaction)
        .filter(Transaction.created_at.between(date_from, date_to))
        .options(joinedload(Transaction.type))
    )
    income = 0
    expenses = 0
    for obj in objs:
        if obj.type.name == "income":
            income += obj.amount
        else:
            expenses += obj.amount
    increase = round(income / expenses, 2)
    # increase = await db_session.scalar(
    #     statement=select(
    #         func.round(
    #             select(func.sum(Transaction.amount)).join(TransactionType)
    #             .filter(TransactionType.name == "income").subquery() /
    #             select(func.sum(Transaction.amount)).join(TransactionType)
    #             .filter(TransactionType.name == "expenses").subquery(),
    #             2
    #         )
    #     )
    # )
    return TransactionIntervalStatDTO(
        increase=increase,
        transactions=[
            TransactionDTO.model_validate(obj=obj, from_attributes=True)
            for obj in objs
        ]
    )
