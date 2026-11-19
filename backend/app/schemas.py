from datetime import date
from decimal import Decimal

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models import AccountType, Interval


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- Auth ----------
class CurrentUser(BaseModel):
    """Eingeloggter Nutzer, ausgelesen aus dem Supabase-Token."""

    id: UUID
    email: str | None = None


# ---------- Konten ----------
class AccountCreate(BaseModel):
    name: str
    type: AccountType = AccountType.CHECKING
    currency: str = "EUR"
    opening_balance: Decimal = Decimal("0")


class AccountRead(ORMModel):
    id: int
    name: str
    type: AccountType
    currency: str
    opening_balance: Decimal


# ---------- Kategorien ----------
class CategoryCreate(BaseModel):
    name: str
    parent_id: int | None = None
    color: str | None = None


class CategoryRead(ORMModel):
    id: int
    name: str
    parent_id: int | None
    color: str | None


# ---------- Buchungen ----------
class TransactionCreate(BaseModel):
    account_id: int
    category_id: int | None = None
    booking_date: date
    amount: Decimal
    description: str = ""
    counterparty: str | None = None


class TransactionRead(ORMModel):
    id: int
    account_id: int
    category_id: int | None
    booking_date: date
    amount: Decimal
    description: str
    counterparty: str | None


# ---------- Budgets ----------
class BudgetCreate(BaseModel):
    category_id: int
    month: date
    limit_amount: Decimal


class BudgetRead(ORMModel):
    id: int
    category_id: int
    month: date
    limit_amount: Decimal


class BudgetStatus(BaseModel):
    """Budget mit aktuellem Verbrauch (für die Ampel-Anzeige)."""

    budget: BudgetRead
    spent: Decimal
    status: str  # "ok" | "warning" | "exceeded"


# ---------- Fixkosten ----------
class RecurringPaymentCreate(BaseModel):
    account_id: int
    category_id: int | None = None
    name: str
    amount: Decimal
    interval: Interval = Interval.MONTHLY
    next_due_date: date


class RecurringPaymentRead(ORMModel):
    id: int
    account_id: int
    category_id: int | None
    name: str
    amount: Decimal
    interval: Interval
    next_due_date: date


# ---------- Sparziele ----------
class SavingsGoalCreate(BaseModel):
    name: str
    target_amount: Decimal
    current_amount: Decimal = Decimal("0")
    target_date: date | None = None


class SavingsGoalRead(ORMModel):
    id: int
    name: str
    target_amount: Decimal
    current_amount: Decimal
    target_date: date | None


# ---------- Szenarien ----------
class ScenarioCreate(BaseModel):
    name: str
    description: str | None = None
    monthly_delta: Decimal = Decimal("0")
    one_time_amount: Decimal = Decimal("0")
    start_date: date


class ScenarioRead(ORMModel):
    id: int
    name: str
    description: str | None
    monthly_delta: Decimal
    one_time_amount: Decimal
    start_date: date


# ---------- Auswertung & Prognose ----------
class MonthlySummary(BaseModel):
    month: date
    income: Decimal
    expenses: Decimal


class CategorySummary(BaseModel):
    category_id: int | None
    category_name: str
    total: Decimal


class ForecastPoint(BaseModel):
    day: date
    balance: Decimal
    is_forecast: bool  # False = echter Kontostand, True = Prognose


class Shortfall(BaseModel):
    """Zeitpunkt, an dem der Kontostand unter den Mindestpuffer fällt."""

    day: date
    balance: Decimal
    buffer: Decimal


class ImportResult(BaseModel):
    imported: int
    skipped: int
