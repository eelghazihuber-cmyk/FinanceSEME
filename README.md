# FinanceSEME

Finanzverwaltung mit Auswertung und Liquiditätsplanung.
Stand: **Machbarkeitsstudie**. Funktioniert schon:

- Registrieren und Anmelden über Supabase, das Backend prüft das Token
- Konten, Kategorien und Buchungen anlegen, anzeigen, löschen
- Übersicht mit Kontostand, Einnahmen/Ausgaben pro Monat und Liquiditätsverlauf
- Einfache Prognose (Durchschnitt der letzten 3 Monate) mit Warnung bei Engpass

Noch offen: CSV-Import, Budgets, Fixkosten, Sparziele, Szenarien, Belege.

## Aufbau

| Teil | Technik | Läuft bei |
|---|---|---|
| Frontend | React + Vite | Vercel (eigenes Projekt, Ordner `frontend`) |
| Backend | Python, FastAPI | Vercel (eigenes Projekt, Ordner `backend`) |
| Datenbank + Login | Supabase (PostgreSQL) | Supabase |

```
financesme/
├── backend/
│   ├── alembic/            # Datenbank-Migrationen (Tabellen anlegen/ändern)
│   ├── api/index.py        # Einstieg für Vercel
│   ├── vercel.json         # leitet alle Anfragen an api/index.py
│   └── app/
│       ├── main.py         # App-Start, Router einbinden
│       ├── config.py       # Einstellungen aus .env
│       ├── database.py     # DB-Verbindung
│       ├── deps.py         # Token prüfen -> eingeloggter Nutzer
│       ├── models.py       # Tabellen (SQLAlchemy)
│       ├── schemas.py      # Ein-/Ausgabe-Formate (Pydantic)
│       ├── routers/        # API-Endpunkte
│       └── services/       # Fachlogik
└── frontend/
    └── src/
        ├── pages/          # Seiten
        ├── components/     # Bausteine
        ├── api/client.js   # Aufrufe ans Backend (schickt Token mit)
        └── lib/supabase.js # Supabase-Login
```

## Einrichten (Windows)

### 1. Supabase-Projekt
1. Auf supabase.com ein Projekt anlegen, Region **Frankfurt**.
2. **Connect → Session pooler**: Adresse kopieren (beginnt mit `postgresql://`).
3. **Project Settings → API**: Projekt-URL und öffentlichen Schlüssel (anon/publishable) kopieren.

### 2. Backend
```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
In `backend\.env` die Werte aus Schritt 1 eintragen. Dann Tabellen anlegen und starten:
```
alembic upgrade head
uvicorn app.main:app --reload
```
- Die Tabellen erscheinen im Supabase-Dashboard unter **Table Editor**.
- API-Doku: http://localhost:8000/docs

### 3. Frontend
```
cd frontend
npm install
copy .env.example .env
npm run dev
```
In `frontend\.env` Projekt-URL und öffentlichen Schlüssel eintragen. App: http://localhost:5173

## Tabellen ändern (später)
1. Klasse in `backend/app/models.py` ändern
2. `alembic revision --autogenerate -m "was geändert wurde"`
3. Neue Datei in `alembic/versions/` kurz prüfen
4. `alembic upgrade head`

Neue Tabellen brauchen in der Migration zusätzlich
`op.execute('ALTER TABLE "<name>" ENABLE ROW LEVEL SECURITY')`.
Sonst sind sie über die automatische Supabase-API mit dem öffentlichen Schlüssel lesbar.

## Online stellen mit Vercel

Ausführliche Anleitung mit Diagrammen und allen Umgebungsvariablen: [docs/HOSTING.md](docs/HOSTING.md)

Zwei Vercel-Projekte aus demselben GitHub-Repository: eins für das Backend, eins für das Frontend.
Jeder Push auf `main` geht danach automatisch online.

### Backend
1. Vercel → **Add New → Project** → Repository `FinanceSEME` importieren.
2. **Root Directory:** `backend` (Framework: Other).
3. **Environment Variables:** `DATABASE_URL`, `SUPABASE_URL` (und `SUPABASE_JWT_SECRET`, falls ihr den geheimen Schlüssel nutzt).
   `CORS_ORIGINS` erst nach dem Frontend eintragen (siehe unten).
4. Deploy. Test: `https://<backend-adresse>/health` zeigt `{"status":"ok"}`.

### Frontend
1. Noch einmal **Add New → Project** mit demselben Repository.
2. **Root Directory:** `frontend` (Framework: Vite, wird erkannt).
3. **Environment Variables:** `VITE_API_URL` = Backend-Adresse, `VITE_SUPABASE_URL`, `VITE_SUPABASE_KEY`.
4. Deploy.

### Verbinden
1. Beim Backend-Projekt `CORS_ORIGINS` setzen, z. B. `["http://localhost:5173","https://<frontend-adresse>"]`, dann **Redeploy**.
2. In Supabase unter **Authentication → URL Configuration** die Frontend-Adresse als Site URL eintragen
   (für den Link in der Bestätigungs-Mail).

Geänderte `VITE_...`-Variablen wirken erst nach einem neuen Deploy des Frontends.

## Wichtig
- `.env`-Dateien niemals nach Git (stehen in `.gitignore`).
- Ins Frontend nur den **öffentlichen** Supabase-Schlüssel, nie den geheimen.
