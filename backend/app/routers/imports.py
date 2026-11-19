from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import get_current_user
from app.schemas import CurrentUser
from app.utils import todo

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/csv", response_model=schemas.ImportResult)
def import_csv(
    account_id: int,
    file: UploadFile,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Kontoauszug als CSV hochladen."""
    todo()
