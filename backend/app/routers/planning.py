"""Planung: Fixkosten, Sparziele und Szenarien."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import get_current_user
from app.schemas import CurrentUser
from app.utils import todo

router = APIRouter(tags=["planning"])


# ---------- Fixkosten & Abos ----------
@router.get("/recurring", response_model=list[schemas.RecurringPaymentRead])
def list_recurring(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    todo()


@router.post("/recurring", response_model=schemas.RecurringPaymentRead)
def create_recurring(
    data: schemas.RecurringPaymentCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    todo()


@router.delete("/recurring/{recurring_id}")
def delete_recurring(
    recurring_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    todo()


# ---------- Sparziele ----------
@router.get("/goals", response_model=list[schemas.SavingsGoalRead])
def list_goals(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    todo()


@router.post("/goals", response_model=schemas.SavingsGoalRead)
def create_goal(
    data: schemas.SavingsGoalCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    todo()


@router.delete("/goals/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    todo()


# ---------- Szenarien ----------
@router.get("/scenarios", response_model=list[schemas.ScenarioRead])
def list_scenarios(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    todo()


@router.post("/scenarios", response_model=schemas.ScenarioRead)
def create_scenario(
    data: schemas.ScenarioCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    todo()


@router.delete("/scenarios/{scenario_id}")
def delete_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    todo()
