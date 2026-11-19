from uuid import UUID
from sqlalchemy.orm import Session

from app.models import Category, Transaction


class CategorizerService:
    """Ordnet Buchungen automatisch einer Kategorie zu."""

    def __init__(self, db: Session):
        self.db = db

    def suggest_category(self, transaction: Transaction) -> Category | None:
        """Schlägt anhand von Text und Empfänger eine Kategorie vor."""
        raise NotImplementedError

    def apply_to_all_uncategorized(self, user_id: UUID) -> int:
        """Kategorisiert alle Buchungen ohne Kategorie. Gibt die Anzahl zurück."""
        raise NotImplementedError
