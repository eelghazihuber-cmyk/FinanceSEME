from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models import Account, Category, Transaction
from app.schemas import BudgetStatus, CategorySummary, MonthlySummary


def month_starts(date_from: date, date_to: date) -> list[date]:
    """Alle Monatsersten von date_from bis date_to."""
    months, current = [], date(date_from.year, date_from.month, 1)
    while current <= date_to:
        months.append(current)
        current = date(current.year + current.month // 12, current.month % 12 + 1, 1)
    return months


class ReportService:
    """Auswertungen für das Dashboard."""

    def __init__(self, db: Session):
        self.db = db

    def income_vs_expenses(self, user_id: UUID, date_from: date, date_to: date) -> list[MonthlySummary]:
        month = func.date_trunc("month", Transaction.booking_date)
        rows = self.db.execute(
            select(
                month,
                func.sum(case((Transaction.amount > 0, Transaction.amount), else_=0)),
                func.sum(case((Transaction.amount < 0, -Transaction.amount), else_=0)),
            )
            .join(Account)
            .where(Account.user_id == user_id, Transaction.booking_date.between(date_from, date_to))
            .group_by(month)
        ).all()
        totals = {m.date(): (income, expenses) for m, income, expenses in rows}
        # Monate ohne Buchungen mit 0 auffüllen, damit das Diagramm keine Lücken hat
        return [
            MonthlySummary(month=m, income=totals.get(m, (0, 0))[0], expenses=totals.get(m, (0, 0))[1])
            for m in month_starts(date_from, date_to)
        ]

    def by_category(self, user_id: UUID, date_from: date, date_to: date) -> list[CategorySummary]:
        rows = self.db.execute(
            select(Transaction.category_id, Category.name, func.sum(-Transaction.amount))
            .join(Account)
            .outerjoin(Category, Transaction.category_id == Category.id)
            .where(
                Account.user_id == user_id,
                Transaction.amount < 0,
                Transaction.booking_date.between(date_from, date_to),
            )
            .group_by(Transaction.category_id, Category.name)
            .order_by(func.sum(-Transaction.amount).desc())
        ).all()
        return [
            CategorySummary(category_id=cid, category_name=name or "Ohne Kategorie", total=Decimal(total))
            for cid, name, total in rows
        ]

    def budget_status(self, user_id: UUID, month: date) -> list[BudgetStatus]:
        raise NotImplementedError  # Phase 4

    def kpis(self, user_id: UUID, month: date) -> dict:
        """Sparquote, Fixkostenquote, Reichweite."""
        raise NotImplementedError  # Phase 4
