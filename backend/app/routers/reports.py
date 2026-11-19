from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import get_current_user
from app.schemas import CurrentUser
from app.services.report_service import ReportService
from app.utils import todo

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly", response_model=list[schemas.MonthlySummary])
def income_vs_expenses(
    date_from: date,
    date_to: date,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Einnahmen und Ausgaben pro Monat."""
    return ReportService(db).income_vs_expenses(user.id, date_from, date_to)


@router.get("/by-category", response_model=list[schemas.CategorySummary])
def by_category(
    date_from: date,
    date_to: date,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Ausgaben nach Kategorie."""
    return ReportService(db).by_category(user.id, date_from, date_to)


@router.get("/kpis")
def kpis(
    month: date,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Sparquote, Fixkostenquote, Reichweite."""
    todo()
