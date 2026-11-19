from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import get_current_user
from app.schemas import CurrentUser
from app.utils import todo

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("/", response_model=list[schemas.BudgetRead])
def list_budgets(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    todo()


@router.get("/status", response_model=list[schemas.BudgetStatus])
def budget_status(
    month: date,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Alle Budgets eines Monats mit Verbrauch und Ampel."""
    todo()


@router.post("/", response_model=schemas.BudgetRead)
def create_budget(
    data: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    todo()


@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    todo()
