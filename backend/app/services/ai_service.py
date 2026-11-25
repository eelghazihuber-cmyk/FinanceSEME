from datetime import date
from uuid import UUID

from google import genai
from sqlalchemy.orm import Session

from app.config import settings
from app.services.report_service import ReportService

MODEL = "gemini-3.8-flash"
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
    """Machbarkeitstest: Ausgaben pro Kategorie von Google Gemini bewerten lassen."""

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

        client = genai.Client(api_key=settings.gemini_api_key)
        interaction = client.interactions.create(
            model=MODEL,
            system_instruction=SYSTEM_PROMPT,
            input=prompt,
            generation_config={
                # Zählt auch die Denk-Tokens mit, darum wenig Denken ("minimal" kann dieses Modell nicht)
                "max_output_tokens": 400,
                "thinking_level": "low",
            },
        )
        return (interaction.output_text or "").strip()
