from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout
from datetime import date
from uuid import UUID

from google import genai
from sqlalchemy.orm import Session

from app.config import settings
from app.services.report_service import ReportService

# "-latest"-Namen findet die API nur unter der Version v1beta
MODEL = "gemini-flash-lite-latest"
API_VERSION = "v1beta"
TIMEOUT_SECONDS = 25
SYSTEM_PROMPT = (
    "Du bist das Frühwarnsystem der App FinanceSEME. Analysiere die Ausgaben kurz auf Deutsch "
    "und nenne auffällige Punkte als Warnung. Erfinde keine Zahlen."
)


class AiTimeout(Exception):
    """Gemini hat nicht innerhalb von TIMEOUT_SECONDS geantwortet."""


# Eigene Threads für die Gemini-Aufrufe, damit wir nach TIMEOUT_SECONDS aufgeben können
_executor = ThreadPoolExecutor(max_workers=4)


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

        future = _executor.submit(self._ask_gemini, prompt)
        try:
            return future.result(timeout=TIMEOUT_SECONDS)
        except FutureTimeout:
            future.cancel()
            raise AiTimeout()
        except Exception as e:
            # Greift das HTTP-Timeout des SDK zuerst, kommt z. B. httpx.ReadTimeout
            if "timeout" in type(e).__name__.lower():
                raise AiTimeout() from e
            raise

    @staticmethod
    def _ask_gemini(prompt: str) -> str:
        client = genai.Client(
            api_key=settings.gemini_api_key,
            # Keine Wiederholungen, sonst würde ein Hänger mehrfach gewartet
            http_options={
                "api_version": API_VERSION,
                "timeout": TIMEOUT_SECONDS * 1000,
                "retry_options": {"attempts": 1},
            },
        )
        interaction = client.interactions.create(
            model=MODEL,
            system_instruction=SYSTEM_PROMPT,
            input=prompt,
            generation_config={
                # Zählt auch die Denk-Tokens mit, darum so wenig Denken wie möglich
                "max_output_tokens": 400,
                "thinking_level": "minimal",
            },
        )
        return (interaction.output_text or "").strip()
