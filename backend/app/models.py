import enum
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Numeric, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Nutzerkonten verwaltet Supabase (Tabelle auth.users).
# Unsere Tabellen speichern nur die Nutzer-ID (UUID) aus dem Token.


class AccountType(str, enum.Enum):
    CHECKING = "checking"   # Girokonto
    SAVINGS = "savings"     # Sparkonto
    CARD = "card"           # Kreditkarte
    CASH = "cash"           # Bargeld


class Interval(str, enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, index=True)  # Supabase-Nutzer (auth.users)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[AccountType] = mapped_column(Enum(AccountType, name="account_type"), default=AccountType.CHECKING)
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    opening_balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account")
    recurring_payments: Mapped[list["RecurringPayment"]] = relationship(back_populates="account")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, index=True)  # Supabase-Nutzer (auth.users)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)



class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    booking_date: Mapped[date] = mapped_column(Date, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))  # Einnahme +, Ausgabe -
    description: Mapped[str] = mapped_column(String(255), default="")
    counterparty: Mapped[str | None] = mapped_column(String(255), nullable=True)

    account: Mapped[Account] = relationship(back_populates="transactions")
    category: Mapped[Category | None] = relationship()
    receipts: Mapped[list["Receipt"]] = relationship(back_populates="transaction")


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"))
    file_path: Mapped[str] = mapped_column(String(500))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    transaction: Mapped[Transaction] = relationship(back_populates="receipts")


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, index=True)  # Supabase-Nutzer (auth.users)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    month: Mapped[date] = mapped_column(Date)  # immer der 1. des Monats
    limit_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    category: Mapped[Category] = relationship()


class RecurringPayment(Base):
    """Fixkosten, Abos und regelmäßige Einnahmen."""

    __tablename__ = "recurring_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    interval: Mapped[Interval] = mapped_column(Enum(Interval, name="payment_interval"), default=Interval.MONTHLY)  # "interval" ist in PostgreSQL schon vergeben
    next_due_date: Mapped[date] = mapped_column(Date)

    account: Mapped[Account] = relationship(back_populates="recurring_payments")


class SavingsGoal(Base):
    __tablename__ = "savings_goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, index=True)  # Supabase-Nutzer (auth.users)
    name: Mapped[str] = mapped_column(String(100))
    target_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    current_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)


class Scenario(Base):
    """Was-wäre-wenn-Rechnung für die Prognose."""

    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, index=True)  # Supabase-Nutzer (auth.users)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    monthly_delta: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)  # z. B. +300 Gehalt
    one_time_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)  # z. B. -15000 Auto
    start_date: Mapped[date] = mapped_column(Date)
