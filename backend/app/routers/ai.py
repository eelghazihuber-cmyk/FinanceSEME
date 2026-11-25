import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.schemas import CurrentUser
from app.services.ai_service import AiService, AiTimeout

log = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/analyse")
def analyse(
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """KI-Frühwarnung zu den Ausgaben der letzten 3 Monate (Machbarkeitstest)."""
    if not settings.gemini_api_key:
        raise HTTPException(status_code=503, detail="KI nicht eingerichtet")
    try:
        answer = AiService(db).analyse(user.id)
    except AiTimeout:
        raise HTTPException(status_code=504, detail="KI antwortet nicht rechtzeitig")
    except Exception:
        log.exception("KI-Analyse fehlgeschlagen")
        raise HTTPException(status_code=502, detail="KI-Dienst nicht erreichbar")
    return {"answer": answer}
