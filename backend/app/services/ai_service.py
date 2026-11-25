from datetime import date
from uuid import UUID

import anthropic
from sqlalchemy.orm import Session

from app.config import settings
from app.services.report_service import ReportService

MODEL = "claude-haiku-5-5"
SYSTEM_PROMPT = (
    "Du bist das Frühwarnsystem der App FinanceSEME. Analysiere die Ausgaben kurz auf Deutsch "
    "und nenne auffällige Punkte als Warnung. Erfinde keine Zahlen."
)


def three_months_ago(today: date) -> date:
    """Gleicher Tag vor 3 Monaten (bei kurzen Monaten der letzte gültige Tag)."""
    month = today.month - 3
    year = today.year
    if month < 1:
        month += 12
        year -= 1
    for day in (today.day, 30, 29, 28):
        try:
            return date(year, month, day)
        except ValueError:
            continue
    raise ValueError("Ungültiges Datum")


class AiService:
    """Machbarkeitstest: Ausgaben pro Kategorie von Claude bewerten lassen."""

    def __init__(self, db: Session):
        self.db = db

    def analyse(self, user_id: UUID) -> str:
        today = date.today()
        date_from = three_months_ago(today)
        categories = ReportService(self.db).by_category(user_id, date_from, today)

        if not categories:
            return "In den letzten 3 Monaten gibt es keine Ausgaben, die man analysieren könnte."

        lines = "\n".join(f"- {c.category_name}: {c.total} EUR" for c in categories)
        prompt = f"Meine Ausgaben pro Kategorie vom {date_from} bis {today}:\n{lines}"

        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            # Ohne Denkphase, damit die 400 Tokens ganz für die Antwort reichen
            thinking={"type": "disabled"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in response.content if block.type == "text").strip()
