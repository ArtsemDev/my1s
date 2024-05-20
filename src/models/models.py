from sqlalchemy import Column, CHAR, VARCHAR, SMALLINT, BIGINT, ForeignKey, DECIMAL, DATE
from sqlalchemy.orm import relationship
from ulid import ULID

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(length=26), primary_key=True, default=lambda: f"{ULID()}")
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(CHAR(length=60), nullable=False)

    def __str__(self) -> str:
        return self.email


class TransactionType(Base):
    __tablename__ = "transaction_types"

    id = Column(SMALLINT, primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)

    transactions = relationship(argument="Transaction", back_populates="type")

    def __str__(self) -> str:
        return self.name


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(
        CHAR(length=26),
        ForeignKey(column=User.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    amount = Column(DECIMAL(precision=12, scale=2), nullable=False)
    type_id = Column(
        SMALLINT,
        ForeignKey(column=TransactionType.id, onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True
    )
    created_at = Column(DATE, nullable=False)

    type = relationship(argument=TransactionType, back_populates="transactions")
