# FinanceSEME – Hinweise für Claude Code

Gruppenprojekt (HTL): Web-App zur Finanzverwaltung mit Auswertung und Liquiditätsprognose.
Abgabe: 15.04.2027. Antworte auf Deutsch, einfach und kurz.

## Stack
- Frontend: React 18 + Vite, Diagramme mit Recharts (`frontend/`)
- Backend: Python, FastAPI, SQLAlchemy 2, Pydantic (`backend/app/`)
- Datenbank + Login: Supabase (PostgreSQL, Region Frankfurt). Login läuft im Frontend über Supabase,
  das Backend prüft nur das Token (`app/services/auth_service.py`, `app/deps.py`).
- Migrationen: Alembic (`backend/alembic/`)
- Hosting: Vercel, zwei Projekte (Root `backend` und Root `frontend`), siehe README

## Aufbau Backend
- `routers/` nimmt Anfragen an und prüft sie, keine Rechenlogik
- `services/` macht die Arbeit (Import, Auswertung, Prognose)
- `models.py` Tabellen, `schemas.py` Ein-/Ausgabeformate
- Jede Abfrage filtert auf den eingeloggten Nutzer (`user.id`), fremde Daten → 404

## Regeln
- Geldbeträge immer `Decimal` / `NUMERIC(12,2)`, nie `float`
- Tabellen nur über Alembic ändern: `alembic revision --autogenerate -m "..."`, prüfen, `alembic upgrade head`
- Neue Tabellen in der Migration mit `ENABLE ROW LEVEL SECURITY` sperren
- `.env` nie committen; ins Frontend nur den öffentlichen Supabase-Schlüssel
- Noch nicht gebaute Endpunkte rufen `todo()` auf (Antwort 501)

## Befehle
- Backend: `cd backend`, `.venv\Scripts\activate`, `uvicorn app.main:app --reload` (Doku: http://localhost:8000/docs)
- Frontend: `cd frontend`, `npm run dev` (http://localhost:5173)

## Stand (19.11.2026): Machbarkeitsstudie
Fertig: Login, Konten, Kategorien, Buchungen, Monatsauswertung, einfache Prognose (Durchschnitt 3 Monate).

## Meilensteine
| | Inhalt | Plan |
|---|---|---|
| M1 | Gerüst und Datenbank (Supabase, Alembic, Aufgaben verteilt) | 20.11.2026 |
| M2 | Login und Buchungen | 18.12.2026 |
| M3 | CSV-Import mit automatischer Kategorisierung | 29.01.2027 |
| M4 | Dashboard und Budgets mit Ampel | 26.02.2027 |
| M5 | Prognose mit Fixkosten und Szenarien | 02.04.2027 |
| M6 | Tests, Doku, Abgabe | 15.04.2027 |
