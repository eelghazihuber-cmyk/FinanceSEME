from typing import BinaryIO

from sqlalchemy.orm import Session

from app.schemas import ImportResult, TransactionCreate


class CsvImportService:
    """Liest Kontoauszüge aus CSV-Dateien ein."""

    def __init__(self, db: Session):
        self.db = db

    def parse(self, file: BinaryIO, account_id: int) -> list[TransactionCreate]:
        """CSV lesen und in Buchungen umwandeln (Spalten erkennen)."""
        raise NotImplementedError

    def remove_duplicates(self, rows: list[TransactionCreate]) -> list[TransactionCreate]:
        """Bereits vorhandene Buchungen herausfiltern."""
        raise NotImplementedError

    def run(self, file: BinaryIO, account_id: int) -> ImportResult:
        """Kompletter Import: lesen, Duplikate prüfen, speichern, kategorisieren."""
        raise NotImplementedError
