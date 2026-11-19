from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import get_current_user
from app.schemas import CurrentUser
from app.services.forecast_service import ForecastService
from app.utils import todo

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.get("/", response_model=list[schemas.ForecastPoint])
def liquidity_forecast(
    months_ahead: int = Query(6, ge=1, le=24),
    scenario_id: int | None = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Kontostand-Verlauf: echte Daten bis heute, danach Prognose."""
    if scenario_id is not None:
        todo()  # Szenarien kommen in Phase 5
    service = ForecastService(db)
    return service.history(user.id) + service.project(user.id, months_ahead)


@router.get("/shortfalls", response_model=list[schemas.Shortfall])
def shortfalls(
    buffer: Decimal = Decimal("0"),
    months_ahead: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Zeitpunkte, an denen der Kontostand unter den Puffer fällt."""
    service = ForecastService(db)
    return service.find_shortfalls(service.project(user.id, months_ahead), buffer)
