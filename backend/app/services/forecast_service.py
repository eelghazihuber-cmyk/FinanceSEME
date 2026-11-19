import calendar
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Account, Scenario, Transaction
from app.schemas import ForecastPoint, Shortfall

CENT = Decimal("0.01")


def add_months(d: date, n: int) -> date:
    y, m = divmod(d.month - 1 + n, 12)
    year, month = d.year + y, m + 1
    return date(year, month, min(d.day, calendar.monthrange(year, month)[1]))


class ForecastService:
    """Liquiditätsverlauf und Prognose (das Kernfeature).

    Machbarkeitsstudie: Die Prognose schreibt den Durchschnitt der letzten
    3 Monate fort. In Phase 5 kommen Fixkosten, Budgets und Szenarien dazu.
    """

    def __init__(self, db: Session):
        self.db = db

    def history(self, user_id: UUID, today: date | None = None) -> list[ForecastPoint]:
        """Echter Kontostand-Verlauf aus Startsalden und Buchungen."""
        today = today or date.today()
        balance = Decimal(
            self.db.scalar(select(func.coalesce(func.sum(Account.opening_balance), 0)).where(Account.user_id == user_id))
        )
        rows = self.db.execute(
            select(Transaction.booking_date, func.sum(Transaction.amount))
            .join(Account)
            .where(Account.user_id == user_id, Transaction.booking_date <= today)
            .group_by(Transaction.booking_date)
            .order_by(Transaction.booking_date)
        ).all()
        points = []
        for day, amount in rows:
            balance += amount
            points.append(ForecastPoint(day=day, balance=balance, is_forecast=False))
        if not points or points[-1].day < today:
            points.append(ForecastPoint(day=today, balance=balance, is_forecast=False))
        return points

    def project(self, user_id: UUID, months_ahead: int, today: date | None = None) -> list[ForecastPoint]:
        """Erwarteter Kontostand: Durchschnitt der letzten 3 Monate fortgeschrieben."""
        today = today or date.today()
        start = self.history(user_id, today)[-1].balance
        last_90_days = Decimal(
            self.db.scalar(
                select(func.coalesce(func.sum(Transaction.amount), 0))
                .join(Account)
                .where(
                    Account.user_id == user_id,
                    Transaction.booking_date > today - timedelta(days=90),
                    Transaction.booking_date <= today,
                )
            )
        )
        per_month = last_90_days / 3
        return [
            ForecastPoint(day=add_months(today, i), balance=(start + per_month * i).quantize(CENT), is_forecast=True)
            for i in range(1, months_ahead + 1)
        ]

    def apply_scenario(self, points: list[ForecastPoint], scenario: Scenario) -> list[ForecastPoint]:
        """Was-wäre-wenn: Szenario auf die Prognose anwenden."""
        raise NotImplementedError  # Phase 5

    def find_shortfalls(self, points: list[ForecastPoint], buffer: Decimal) -> list[Shortfall]:
        """Prognose-Zeitpunkte, an denen der Stand unter den Puffer fällt."""
        return [
            Shortfall(day=p.day, balance=p.balance, buffer=buffer)
            for p in points
            if p.is_forecast and p.balance < buffer
        ]
