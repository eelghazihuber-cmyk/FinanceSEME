"""Einstieg für Vercel: Vercel startet diese Datei und findet darin die FastAPI-App."""

import pathlib
import sys

# Ordner "backend" in den Suchpfad, damit "import app" funktioniert
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from app.main import app  # noqa: E402,F401
