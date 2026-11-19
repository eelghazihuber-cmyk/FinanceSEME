# Changelog

Neueste Einträge oben.

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
