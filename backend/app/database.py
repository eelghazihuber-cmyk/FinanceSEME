from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings

# NullPool: jede Anfrage öffnet eine eigene Verbindung und schließt sie wieder.
# Passt zu Vercel, wo das Backend nicht dauerhaft läuft. Supabase bündelt die
# Verbindungen ohnehin im "Session pooler".
engine = create_engine(settings.sqlalchemy_url, poolclass=NullPool)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Basisklasse aller Datenbank-Tabellen."""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
