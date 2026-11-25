# Changelog

Neueste Einträge oben.

## 2026-11-25 – KI-Test von Claude auf Google Gemini umgestellt
- Wer: Elias
- Was: Die KI-Analyse (`GET /ai/analyse`) nutzt jetzt Google Gemini (Modell `gemini-3.8-flash`, kostenlose Stufe) statt Claude. Paket `google-genai` statt `anthropic`, Einstellung `gemini_api_key` (Env `GEMINI_API_KEY`) statt `anthropic_api_key`. Max. 400 Ausgabe-Tokens, Denken auf "low", weil Gemini die Denk-Tokens mitzählt. Systemprompt, Endpunkt, 503 ohne Schlüssel und der Button bleiben gleich. Fehler beim KI-Dienst werden geloggt und mit 502 beantwortet.
- Warum: Gemini hat eine kostenlose Stufe, das passt besser zum Schulprojekt. Achtung: In der kostenlosen Stufe darf Google die Eingaben zur Verbesserung seiner Produkte verwenden.
- Bereiche: `backend/app/services/ai_service.py`, `backend/app/routers/ai.py`, `backend/app/config.py`, `backend/requirements.txt`, `backend/.env.example`, `frontend/src/pages/Dashboard.jsx`

## 2026-11-25 – Erster KI-Test (Frühwarnung)
- Wer: Elias
- Was: Neuer Endpunkt `GET /ai/analyse` (nur mit Login). Er summiert die Ausgaben der letzten 3 Monate pro Kategorie und lässt sie von Claude (Modell `claude-haiku-5-5`, max. 400 Tokens) kurz auf Deutsch bewerten. Ohne `ANTHROPIC_API_KEY` in der `.env` antwortet er mit 503 "KI nicht eingerichtet". Auf der Übersicht gibt es einen Button "KI-Analyse", der den Text anzeigt. Paket `anthropic` in `requirements.txt`.
- Warum: Machbarkeitstest, ob eine KI-Frühwarnung zu den Ausgaben sinnvoll funktioniert. Noch nicht voll ausgebaut.
- Bereiche: `backend/app/services/ai_service.py`, `backend/app/routers/ai.py`, `backend/app/config.py`, `backend/app/main.py`, `backend/requirements.txt`, `backend/.env.example`, `frontend/src/pages/Dashboard.jsx`, `frontend/src/api/client.js`

## 2026-11-20 – Lokale Umgebung eingerichtet und Hosting-Anleitung
- Wer: Elias
- Was: Lokale Entwicklungsumgebung eingerichtet (Python 3.13, Node.js 24, `.venv`, `npm install`, `.env`-Dateien aus den Vorlagen angelegt, aber nicht committet). Mit `alembic upgrade head` die Tabellen in der Supabase-Datenbank angelegt. Backend und Frontend laufen lokal. Neue Anleitung `docs/HOSTING.md` mit Diagrammen zu Supabase, Vercel, Login-Ablauf und allen Umgebungsvariablen. Ordner `docs/bilder/` mit Liste der noch fehlenden Screenshots.
- Warum: Damit alle im Team die App lokal starten können und nachvollziehbar ist, wie das Hosting eingerichtet ist.
- Bereiche: `docs/HOSTING.md`, `docs/bilder/`, `README.md`, Supabase-Datenbank (Migration `0001_erste_tabellen`)

## 2026-11-19 – Changelog eingeführt
- Wer: Elias
- Was: CHANGELOG.md angelegt und die bisherigen Stände eingetragen. In der CLAUDE.md steht jetzt die Regel, dass jede committete Änderung hier eingetragen wird.
- Warum: Damit alle im Team sehen, wer wann was geändert hat und warum.
- Bereiche: `CHANGELOG.md`, `CLAUDE.md`

## 2026-11-19 – Machbarkeitsstudie
- Wer: Elias
- Was: Login, Konten, Kategorien, Buchungen, Monatsauswertung und einfache Prognose (Durchschnitt der letzten 3 Monate) funktionieren. Projekt auf GitHub hochgeladen.
- Warum: Zeigen, dass die geplante Lösung technisch machbar ist.
- Bereiche: `backend/app/`, `frontend/src/`

## 2026-11-12 – Umstellung auf Supabase
- Wer: Elias
- Was: Login und Datenbank laufen jetzt über Supabase. Die eigene users-Tabelle wurde entfernt. Alembic mit der ersten Migration eingerichtet. Docker entfernt, Projekt für Vercel vorbereitet.
- Warum: Weniger eigener Code für Login und Datenbank, einfacheres Hosting ohne eigenen Server.
- Bereiche: `backend/app/`, `backend/alembic/`, `backend/vercel.json`, `frontend/src/lib/supabase.js`, `frontend/vercel.json`

## 2026-10-08 – Erstes Code-Gerüst
- Wer: Elias
- Was: Grundaufbau für Backend (FastAPI) und Frontend (React + Vite) angelegt. Alle Klassen und Endpunkte sind da, aber noch ohne Funktion.
- Warum: Gemeinsame Grundlage, damit das Team die Aufgaben aufteilen und parallel arbeiten kann.
- Bereiche: `backend/`, `frontend/`
