from uuid import UUID
from decimal import Decimal

from sqlalchemy.orm import Session

from app.schemas import Shortfall


class AlertService:
    """Frühwarnung bei Engpässen und überschrittenen Budgets."""

    def __init__(self, db: Session):
        self.db = db

    def check_shortfalls(self, user_id: UUID, buffer: Decimal) -> list[Shortfall]:
        raise NotImplementedError

    def check_budgets(self, user_id: UUID) -> list[str]:
        """Meldungen zu überschrittenen oder knappen Budgets."""
        raise NotImplementedError

    def send(self, user_id: UUID, message: str) -> None:
        """Benachrichtigung zustellen (E-Mail oder Push)."""
        raise NotImplementedError
